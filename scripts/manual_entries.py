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

# Manual entries — top 3 cheapest non-ghost fares per (corridor, date), observed 2026-06-10.
# Today: all 8 HND + all 8 KIX returned inline; NRT 08-01 + ICN 11-25/12-20/01-15 also inline.
# Everything else (incl. NRT x7, ICN 06-15/07-04/07-15/08-01/09-01) saved to files for the aggregator.
MANUAL = [
    # NRT-HNL 08-01 (returned inline)
    ("NRT-HNL", "2026-08-01", [
        {"airline": "Korean Air", "price": 589, "is_nonstop": 0, "duration_mins": 530},
        {"airline": "Korean Air", "price": 589, "is_nonstop": 0, "duration_mins": 530},
        {"airline": "Korean Air", "price": 646, "is_nonstop": 0, "duration_mins": 530},
    ]),

    # HND-HNL (all 8 returned inline)
    ("HND-HNL", "2026-06-15", [
        {"airline": "Alaska Airlines", "price": 395, "is_nonstop": 1, "duration_mins": 475},
        {"airline": "Alaska Airlines", "price": 395, "is_nonstop": 1, "duration_mins": 475},
        {"airline": "Japan Airlines", "price": 432, "is_nonstop": 0, "duration_mins": 510},
    ]),
    ("HND-HNL", "2026-07-04", [
        {"airline": "Delta Air Lines", "price": 374, "is_nonstop": 1, "duration_mins": 473},
        {"airline": "Alaska Airlines", "price": 605, "is_nonstop": 1, "duration_mins": 475},
        {"airline": "Alaska Airlines", "price": 605, "is_nonstop": 1, "duration_mins": 475},
    ]),
    ("HND-HNL", "2026-07-15", [
        {"airline": "Alaska Airlines", "price": 533, "is_nonstop": 1, "duration_mins": 475},
        {"airline": "Korean Air", "price": 543, "is_nonstop": 0, "duration_mins": 530},
        {"airline": "Korean Air", "price": 552, "is_nonstop": 0, "duration_mins": 530},
    ]),
    ("HND-HNL", "2026-08-01", [
        {"airline": "Korean Air", "price": 758, "is_nonstop": 0, "duration_mins": 530},
        {"airline": "Korean Air", "price": 767, "is_nonstop": 0, "duration_mins": 530},
        {"airline": "Korean Air", "price": 767, "is_nonstop": 0, "duration_mins": 530},
    ]),
    ("HND-HNL", "2026-09-01", [
        {"airline": "Alaska Airlines", "price": 395, "is_nonstop": 1, "duration_mins": 475},
        {"airline": "Alaska Airlines", "price": 395, "is_nonstop": 1, "duration_mins": 475},
        {"airline": "Delta Air Lines", "price": 450, "is_nonstop": 1, "duration_mins": 470},
    ]),
    ("HND-HNL", "2026-11-25", [
        {"airline": "Alaska Airlines", "price": 449, "is_nonstop": 1, "duration_mins": 435},
        {"airline": "Alaska Airlines", "price": 449, "is_nonstop": 1, "duration_mins": 435},
        {"airline": "Delta Air Lines", "price": 450, "is_nonstop": 1, "duration_mins": 445},
    ]),
    ("HND-HNL", "2026-12-20", [
        {"airline": "Alaska Airlines", "price": 449, "is_nonstop": 1, "duration_mins": 435},
        {"airline": "Alaska Airlines", "price": 449, "is_nonstop": 1, "duration_mins": 435},
        {"airline": "Delta Air Lines", "price": 451, "is_nonstop": 1, "duration_mins": 420},
    ]),
    ("HND-HNL", "2027-01-15", [
        {"airline": "Delta Air Lines", "price": 450, "is_nonstop": 1, "duration_mins": 410},
        {"airline": "Korean Air", "price": 584, "is_nonstop": 0, "duration_mins": 490},
        {"airline": "Korean Air", "price": 589, "is_nonstop": 0, "duration_mins": 490},
    ]),

    # KIX-HNL (all 8 returned inline)
    ("KIX-HNL", "2026-06-15", [
        {"airline": "Japan Airlines", "price": 451, "is_nonstop": 0, "duration_mins": 475},
        {"airline": "Japan Airlines", "price": 451, "is_nonstop": 0, "duration_mins": 475},
        {"airline": "Japan Airlines", "price": 452, "is_nonstop": 0, "duration_mins": 475},
    ]),
    ("KIX-HNL", "2026-07-04", [
        {"airline": "Japan Airlines", "price": 452, "is_nonstop": 0, "duration_mins": 475},
        {"airline": "Japan Airlines", "price": 452, "is_nonstop": 0, "duration_mins": 475},
        {"airline": "Korean Air", "price": 617, "is_nonstop": 0, "duration_mins": 530},
    ]),
    ("KIX-HNL", "2026-07-15", [
        {"airline": "Korean Air", "price": 546, "is_nonstop": 0, "duration_mins": 530},
        {"airline": "Korean Air", "price": 546, "is_nonstop": 0, "duration_mins": 530},
        {"airline": "Korean Air", "price": 546, "is_nonstop": 0, "duration_mins": 530},
    ]),
    ("KIX-HNL", "2026-08-01", [
        {"airline": "Korean Air", "price": 761, "is_nonstop": 0, "duration_mins": 530},
        {"airline": "Korean Air", "price": 761, "is_nonstop": 0, "duration_mins": 530},
        {"airline": "Korean Air", "price": 761, "is_nonstop": 0, "duration_mins": 530},
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
        {"airline": "Korean Air", "price": 587, "is_nonstop": 0, "duration_mins": 490},
        {"airline": "Korean Air", "price": 587, "is_nonstop": 0, "duration_mins": 490},
        {"airline": "Korean Air", "price": 587, "is_nonstop": 0, "duration_mins": 490},
    ]),

    # ICN-HNL 11-25, 12-20, 01-15 (returned inline)
    ("ICN-HNL", "2026-11-25", [
        {"airline": "Perimeter Aviation", "price": 416, "is_nonstop": 1, "duration_mins": 500},
        {"airline": "Korean Air", "price": 483, "is_nonstop": 0, "duration_mins": 435},
        {"airline": "Korean Air", "price": 483, "is_nonstop": 0, "duration_mins": 435},
    ]),
    ("ICN-HNL", "2026-12-20", [
        {"airline": "Korean Air", "price": 550, "is_nonstop": 0, "duration_mins": 455},
        {"airline": "Korean Air", "price": 562, "is_nonstop": 0, "duration_mins": 435},
        {"airline": "Korean Air", "price": 562, "is_nonstop": 0, "duration_mins": 435},
    ]),
    ("ICN-HNL", "2027-01-15", [
        {"airline": "Perimeter Aviation", "price": 519, "is_nonstop": 1, "duration_mins": 500},
        {"airline": "Korean Air", "price": 527, "is_nonstop": 0, "duration_mins": 435},
        {"airline": "Korean Air", "price": 527, "is_nonstop": 0, "duration_mins": 435},
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
