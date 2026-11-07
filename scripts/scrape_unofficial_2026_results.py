#!/usr/bin/env python3
"""Scrape unofficial NYC Board of Elections results for the 2026 governor's race.

Reads https://enr.boenyc.gov/CD27432AD0.html and each assembly-district page,
then writes data/results_2026_governor.csv.

Party lines for the same ticket are kept separate and also summed:
  Hochul   = Democratic + Working Families
  Blakeman = Republican + Conservative + Vote Affordable
"""

from __future__ import annotations

import csv
import re
import subprocess
import sys
from pathlib import Path

INDEX = "https://enr.boenyc.gov/CD27432AD0.html"
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "results_2026_governor.csv"


def fetch(url: str) -> str:
    return subprocess.check_output(
        ["curl", "-fsSL", "-A", "Mozilla/5.0", "--retry", "3", "--max-time", "40", url],
        text=True,
    )


def parse_int(value: str) -> int:
    value = value.strip().replace(",", "")
    if value in {"", "-", "—"}:
        return 0
    return int(value)


def rows_from_page(html: str) -> list[dict[str, int | str]]:
    title = re.search(r"AD\s*(\d+)\s*\]", html)
    if not title:
        return []
    ad = int(title.group(1))
    parsed = []
    for tr in re.findall(r"<tr>(.*?)</tr>", html, flags=re.S | re.I):
        cells = [
            re.sub(r"<[^>]+>", "", cell).replace("&nbsp;", " ").strip()
            for cell in re.findall(r"<td[^>]*>(.*?)</td>", tr, flags=re.S | re.I)
        ]
        if not cells or not cells[0].startswith("ED"):
            continue
        ed = int(cells[0].split()[-1])

        def cell(index: int) -> int:
            return parse_int(cells[index]) if index < len(cells) else 0

        dem, rep, con, wfp, affordable, write_in = (
            cell(3),
            cell(5),
            cell(7),
            cell(9),
            cell(11),
            cell(13),
        )
        hochul = dem + wfp
        blakeman = rep + con + affordable
        parsed.append(
            {
                "elect_dist": ad * 1000 + ed,
                "ad": ad,
                "ed": ed,
                "pct_reported": cells[1] if len(cells) > 1 else "",
                "hochul_democratic": dem,
                "blakeman_republican": rep,
                "blakeman_conservative": con,
                "hochul_working_families": wfp,
                "blakeman_vote_affordable": affordable,
                "write_in": write_in,
                "hochul": hochul,
                "blakeman": blakeman,
                "total": hochul + blakeman + write_in,
            }
        )
    return parsed


def main() -> int:
    index = fetch(INDEX)
    pages = sorted(set(re.findall(r'href="(CD27432AD\d+\.html)"', index)))
    if not pages:
        print("No assembly-district pages found", file=sys.stderr)
        return 1
    rows: list[dict[str, int | str]] = []
    for page in pages:
        rows.extend(rows_from_page(fetch(f"https://enr.boenyc.gov/{page}")))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    hochul = sum(int(row["hochul"]) for row in rows)
    blakeman = sum(int(row["blakeman"]) for row in rows)
    print(f"Wrote {len(rows)} districts to {OUT}")
    print(f"Hochul {hochul:,}  Blakeman {blakeman:,}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
