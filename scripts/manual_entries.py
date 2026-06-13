#!/usr/bin/env python3
"""Merge manually-extracted top-3 fares for inline-response corridors into mcp_flights.json.

These corridors (HND, KIX, ICN origin) often return small inline responses
that do NOT get saved to the session's tool-results dir, so they need manual
population. Duration values mirror the leg duration the aggregator would emit
(last-leg duration for connections, single-leg for nonstops) to stay
consistent with the rest of the dataset.
"""
import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "data" / "mcp_flights.json"

# Manual entries — top 3 cheapest non-ghost fares per (corridor, date), observed 2026-06-13.
# Today: all 8 HND + all 8 KIX returned inline (not saved to files), so they need manual entry.
# NRT (x8) and ICN (x8) were saved to files and picked up by the aggregator — do NOT add them
# here or this overlay would clobber today's fresh file-based data with stale values.
# HND-HNL 2026-12-20 returned 0 results on two attempts (no current availability) — omitted.
MANUAL = [
    # HND-HNL (7 of 8 returned inline; 12-20 empty)
    ("HND-HNL", "2026-06-15", [
        {"airline": "Philippine Airlines", "price": 501, "is_nonstop": 0, "duration_mins": 635},
        {"airline": "Alaska Airlines", "price": 511, "is_nonstop": 1, "duration_mins": 475},
        {"airline": "Alaska Airlines", "price": 596, "is_nonstop": 1, "duration_mins": 475},
    ]),
    ("HND-HNL", "2026-07-04", [
        {"airline": "Delta Air Lines", "price": 375, "is_nonstop": 1, "duration_mins": 473},
        {"airline": "Alaska Airlines", "price": 605, "is_nonstop": 1, "duration_mins": 475},
        {"airline": "Alaska Airlines", "price": 605, "is_nonstop": 1, "duration_mins": 475},
    ]),
    ("HND-HNL", "2026-07-15", [
        {"airline": "Alaska Airlines", "price": 533, "is_nonstop": 1, "duration_mins": 475},
        {"airline": "Korean Air", "price": 544, "is_nonstop": 0, "duration_mins": 530},
        {"airline": "Korean Air", "price": 553, "is_nonstop": 0, "duration_mins": 530},
    ]),
    ("HND-HNL", "2026-08-01", [
        {"airline": "Korean Air", "price": 759, "is_nonstop": 0, "duration_mins": 530},
        {"airline": "Korean Air", "price": 768, "is_nonstop": 0, "duration_mins": 530},
        {"airline": "Korean Air", "price": 768, "is_nonstop": 0, "duration_mins": 530},
    ]),
    ("HND-HNL", "2026-09-01", [
        {"airline": "Alaska Airlines", "price": 395, "is_nonstop": 1, "duration_mins": 475},
        {"airline": "Alaska Airlines", "price": 395, "is_nonstop": 1, "duration_mins": 475},
        {"airline": "Delta Air Lines", "price": 451, "is_nonstop": 1, "duration_mins": 470},
    ]),
    ("HND-HNL", "2026-11-25", [
        {"airline": "Alaska Airlines", "price": 449, "is_nonstop": 1, "duration_mins": 435},
        {"airline": "Alaska Airlines", "price": 449, "is_nonstop": 1, "duration_mins": 435},
        {"airline": "Delta Air Lines", "price": 451, "is_nonstop": 1, "duration_mins": 445},
    ]),
    ("HND-HNL", "2027-01-15", [
        {"airline": "Delta Air Lines", "price": 451, "is_nonstop": 1, "duration_mins": 410},
        {"airline": "Korean Air", "price": 465, "is_nonstop": 0, "duration_mins": 460},
        {"airline": "Korean Air", "price": 553, "is_nonstop": 0, "duration_mins": 460},
    ]),

    # KIX-HNL (all 8 returned inline)
    ("KIX-HNL", "2026-06-15", [
        {"airline": "Korean Air", "price": 606, "is_nonstop": 0, "duration_mins": 525},
        {"airline": "Alaska Airlines", "price": 609, "is_nonstop": 1, "duration_mins": 510},
        {"airline": "Asiana Airlines", "price": 639, "is_nonstop": 0, "duration_mins": 525},
    ]),
    ("KIX-HNL", "2026-07-04", [
        {"airline": "Japan Airlines", "price": 451, "is_nonstop": 0, "duration_mins": 475},
        {"airline": "Japan Airlines", "price": 451, "is_nonstop": 0, "duration_mins": 475},
        {"airline": "Korean Air", "price": 618, "is_nonstop": 0, "duration_mins": 530},
    ]),
    ("KIX-HNL", "2026-07-15", [
        {"airline": "Korean Air", "price": 546, "is_nonstop": 0, "duration_mins": 530},
        {"airline": "Korean Air", "price": 546, "is_nonstop": 0, "duration_mins": 530},
        {"airline": "Korean Air", "price": 546, "is_nonstop": 0, "duration_mins": 530},
    ]),
    ("KIX-HNL", "2026-08-01", [
        {"airline": "Korean Air", "price": 762, "is_nonstop": 0, "duration_mins": 530},
        {"airline": "Korean Air", "price": 762, "is_nonstop": 0, "duration_mins": 530},
        {"airline": "Korean Air", "price": 762, "is_nonstop": 0, "duration_mins": 530},
    ]),
    ("KIX-HNL", "2026-09-01", [
        {"airline": "Japan Airlines", "price": 451, "is_nonstop": 0, "duration_mins": 475},
        {"airline": "Japan Airlines", "price": 451, "is_nonstop": 0, "duration_mins": 475},
        {"airline": "Japan Airlines", "price": 451, "is_nonstop": 0, "duration_mins": 475},
    ]),
    ("KIX-HNL", "2026-11-25", [
        {"airline": "Korean Air", "price": 462, "is_nonstop": 0, "duration_mins": 490},
        {"airline": "Korean Air", "price": 462, "is_nonstop": 0, "duration_mins": 490},
        {"airline": "Korean Air", "price": 462, "is_nonstop": 0, "duration_mins": 490},
    ]),
    ("KIX-HNL", "2026-12-20", [
        {"airline": "Japan Airlines", "price": 505, "is_nonstop": 0, "duration_mins": 435},
        {"airline": "Japan Airlines", "price": 505, "is_nonstop": 0, "duration_mins": 435},
        {"airline": "Japan Airlines", "price": 505, "is_nonstop": 0, "duration_mins": 435},
    ]),
    ("KIX-HNL", "2027-01-15", [
        {"airline": "Korean Air", "price": 559, "is_nonstop": 0, "duration_mins": 490},
        {"airline": "Korean Air", "price": 559, "is_nonstop": 0, "duration_mins": 490},
        {"airline": "Korean Air", "price": 574, "is_nonstop": 0, "duration_mins": 490},
    ]),
]


def main() -> None:
    data = json.loads(OUT.read_text())
    by_key = {(e["corridor"], e["target_date"]): e for e in data}
    for corridor, target_date, fares in MANUAL:
        by_key[(corridor, target_date)] = {
            "corridor": corridor,
            "target_date": target_date,
            "fares": fares,
        }
    merged = sorted(by_key.values(), key=lambda e: (e["corridor"], e["target_date"]))
    OUT.write_text(json.dumps(merged, indent=2))
    print(f"Merged manual entries; total entries: {len(merged)}/80")


if __name__ == "__main__":
    main()
