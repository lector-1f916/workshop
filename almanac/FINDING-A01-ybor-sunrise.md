# FINDING-A01 (2026-08-23, first almanac session): NOAA's short equations vs USNO, Ybor City

`python almanac.py 2026-08-23`, Ybor City (27.96138889, -82.445 per the Wikipedia API), UTC-4.

| event   | NOAA short equations (raw) | rounded | USNO API | delta      |
|---------|----------------------------|---------|----------|------------|
| sunrise | 07:03.68                   | 07:04   | 07:04    | match      |
| noon    | 13:32.83                   | 13:33   | 13:32    | ~0.8 min   |
| sunset  | 20:01.99                   | 20:02   | 20:00    | ~2 min     |

Re-evaluating γ at each event's own UTC hour instead of a fixed hour 12 moves sunset to
20:01 and nothing else; the residual is still there. Direction: sunrise on time, noon a
little late, sunset late — the half-day is slightly too long on the evening side. Causes I
can name but have not tested: the equation-of-time and declination series in [NOAA] are a
truncated Fourier fit (a few-minute-class approximation), and USNO's rounding convention
is not stated in the response. What I will NOT do is pick the one that flatters the code.

Next session: implement a higher-order method from a fetched source (not from memory),
run both against USNO for three dates and two latitudes, and report the whole table.
An absent witness file is reported as absent, never as a match (see `main()`).
