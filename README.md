# NYC 2026 election map

Election-district map of unofficial New York City results for the November 3, 2026 race for governor.

2026 was not a presidential year. This project updates the method behind [toddwschneider/nyc-presidential-election-map](https://github.com/toddwschneider/nyc-presidential-election-map) — Board of Elections returns joined to Department of City Planning election districts — for Kathy Hochul and Bruce Blakeman.

## Citywide (unofficial, about 97% of scanners)

| | Votes | Two-party share |
| --- | ---: | ---: |
| Kathy Hochul / Adrienne Adams | 1,505,223 | 76.3% |
| Bruce Blakeman / Todd Hood | 468,543 | 23.7% |
| Write-in | 4,279 |  |

Party lines are combined for each ticket: Hochul on Democratic and Working Families; Blakeman on Republican, Conservative, and Vote Affordable.

Figures are the Board of Elections election-night report as of November 4, 2026, 12:42 a.m. They are not certified. Absentee and mail ballots were still out.

## Map

`index.html` is the default entry point and displays the map of all 4,214 election districts. Open it with a local static server (fetch will not work from `file://`):

```sh
python3 -m http.server 8000
```

Then visit `http://localhost:8000/`.

District geometry is `data/districts.topojson` (NYC DCP election districts, release 26C, August 2026, clipped to the shoreline). The Board of Elections revised those lines effective April 1, 2026. Every district with recorded votes matched a polygon. Seventy-one reported districts had zero ballots and no polygon; they do not change the totals.

## Data

`data/results_2026_governor.csv` is one row per election district:

- `elect_dist` is assembly district × 1000 + election district (AD 65, ED 1 → `65001`)
- candidate columns are individual party lines
- `hochul` and `blakeman` are the combined totals used to color the map

## Reproduce

```sh
python3 scripts/scrape_unofficial_2026_results.py
```

The script reads the unofficial pages at [enr.boenyc.gov](https://enr.boenyc.gov/) for contest `CD27432` (Governor / Lieutenant Governor). Those pages were the election-night report; they can change or disappear after certification.

## Sources

- Results: [New York City Board of Elections election-night results](https://enr.boenyc.gov/)
- Boundaries: [NYC Planning election districts](https://www.nyc.gov/content/planning/pages/resources/datasets/election-districts), also published as NYC Open Data `wwxk-38u4` (version 26c)
- Method: Todd W. Schneider, NYC presidential election map, 2016–2024
