"""
almanac.py — the fifth hobby (started 2026-08-23). Sunrise, noon and sunset for a place
and a date, computed from NOAA's published equations, then checked against the US Naval
Observatory's API. Two witnesses that do not know about each other: if they agree to the
minute, the arithmetic is right; if they do not, the interesting part is which one is wrong.

Every constant cites its source on the line it is defined. Nothing here is from memory.

Sources (fetched, on disk under sources/):
  [NOAA] "General Solar Position Calculations", NOAA Global Monitoring Division,
         https://gml.noaa.gov/grad/solcalc/solareqns.PDF  (fetched 2026-08-23, HTTP 200,
         208,947 bytes; text in sources/noaa-solareqns.txt). Equations quoted in comments.
  [USNO] https://aa.usno.navy.mil/api/rstt/oneday?date=YYYY-MM-DD&coords=LAT,LON&tz=TZ
         (fetched 2026-08-23, HTTP 200; sources/usno-2026-08-23.json).
  [WP]   Ybor City coordinates from the Wikipedia API (action=query&prop=coordinates,
         fetched 2026-08-23): lat 27.96138889, lon -82.445.
"""
import json
import math
import sys
from datetime import date

# [WP] Ybor City, Tampa: the cigar factories the lector read in.
YBOR_LAT = 27.96138889
YBOR_LON = -82.445          # [NOAA]: "positive to the east of the Prime Meridian"
TZ_TAMPA_AUGUST = -4        # [USNO] response for this date says "tz": -4.0, "isdst": false
                            # (USNO treats the requested tz as the local offset; August Tampa is EDT, UTC-4)
ZENITH_RISE_SET = 90.833    # [NOAA]: "the zenith is set to 90.833° (the approximate correction for
                            #   atmospheric refraction at sunrise and sunset, and the size of the solar disk)"


def fractional_year(d: date, hour: float = 12.0) -> float:
    # [NOAA]: γ = 2π/365 * (day_of_year − 1 + (hour − 12)/24); "For leap years, use 366".
    days = 366 if (d.year % 4 == 0 and (d.year % 100 != 0 or d.year % 400 == 0)) else 365
    return 2 * math.pi / days * (d.timetuple().tm_yday - 1 + (hour - 12) / 24)


def eqtime_minutes(g: float) -> float:
    # [NOAA]: eqtime = 229.18*(0.000075 + 0.001868cos(γ) − 0.032077sin(γ) − 0.014615cos(2γ) − 0.040849sin(2γ))
    return 229.18 * (0.000075 + 0.001868 * math.cos(g) - 0.032077 * math.sin(g)
                     - 0.014615 * math.cos(2 * g) - 0.040849 * math.sin(2 * g))


def declination_rad(g: float) -> float:
    # [NOAA]: decl = 0.006918 − 0.399912cos(γ) + 0.070257sin(γ) − 0.006758cos(2γ) + 0.000907sin(2γ)
    #                − 0.002697cos(3γ) + 0.00148sin(3γ)
    return (0.006918 - 0.399912 * math.cos(g) + 0.070257 * math.sin(g) - 0.006758 * math.cos(2 * g)
            + 0.000907 * math.sin(2 * g) - 0.002697 * math.cos(3 * g) + 0.00148 * math.sin(3 * g))


def rise_noon_set_utc_minutes(d: date, lat: float, lon: float):
    """Returns (sunrise, solar noon, sunset) as minutes after 00:00 UTC, per [NOAA]."""
    g = fractional_year(d)
    eqt = eqtime_minutes(g)
    decl = declination_rad(g)
    lat_r = math.radians(lat)
    # [NOAA]: ha = ±arccos( cos(90.833)/(cos(lat)cos(decl)) − tan(lat)tan(decl) ), "positive ... sunrise"
    cos_ha = (math.cos(math.radians(ZENITH_RISE_SET)) / (math.cos(lat_r) * math.cos(decl))
              - math.tan(lat_r) * math.tan(decl))
    if cos_ha < -1 or cos_ha > 1:
        return None  # polar day or night
    ha = math.degrees(math.acos(cos_ha))
    # [NOAA]: sunrise = 720 − 4*(longitude + ha) − eqtime ; snoon = 720 − 4*longitude − eqtime
    sunrise = 720 - 4 * (lon + ha) - eqt
    sunset = 720 - 4 * (lon - ha) - eqt
    snoon = 720 - 4 * lon - eqt
    return sunrise, snoon, sunset


def hhmm(minutes_utc: float, tz_hours: float) -> str:
    m = (minutes_utc + tz_hours * 60) % 1440
    return f"{int(m // 60):02d}:{int(round(m % 60)):02d}"


def main():
    d = date.fromisoformat(sys.argv[1]) if len(sys.argv) > 1 else date(2026, 8, 23)
    r = rise_noon_set_utc_minutes(d, YBOR_LAT, YBOR_LON)
    rise, noon, sset = (hhmm(x, TZ_TAMPA_AUGUST) for x in r)
    print(f"[NOAA] Ybor City {d}: sunrise {rise}  solar noon {noon}  sunset {sset}  (local, UTC{TZ_TAMPA_AUGUST:+d})")
    try:
        u = json.load(open(f"sources/usno-{d}.json", encoding="utf8"))["properties"]["data"]
        got = {row["phen"]: row["time"] for row in u["sundata"]}
        print(f"[USNO] Ybor City {d}: sunrise {got['Rise']}  upper transit {got['Upper Transit']}  sunset {got['Set']}  (tz {u['tz']})")
        for name, mine, theirs in (("sunrise", rise, got["Rise"]), ("noon", noon, got["Upper Transit"]), ("sunset", sset, got["Set"])):
            print(f"  {name:8s} {'MATCH' if mine == theirs else 'DIFF'}  noaa {mine}  usno {theirs}")
    except FileNotFoundError:
        print(f"[USNO] no sources/usno-{d}.json on disk — fetch it; an absent witness is not a matching one")


if __name__ == "__main__":
    main()
