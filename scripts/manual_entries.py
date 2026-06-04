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

# Manual entries — top 3 cheapest non-ghost fares per (corridor, date), observed 2026-06-04.
# Today: all 8 HND + all 8 KIX returned inline; NRT 08-01, ICN 11-25, ICN 01-15 also inline.
MANUAL = [
    # HND-HNL (all 8 returned inline)
    ("HND-HNL", "2026-06-15", [
        {"airline": "Alaska Airlines", "price": 396, "is_nonstop": 1, "duration_mins": 475},
        {"airline": "Alaska Airlines", "price": 396, "is_nonstop": 1, "duration_mins": 475},
        {"airline": "Japan Airlines", "price": 433, "is_nonstop": 0, "duration_mins": 510},
    ]),
    ("HND-HNL", "2026-07-04", [
        {"airline": "Alaska Airlines", "price": 582, "is_nonstop": 1, "duration_mins": 475},
        {"airline": "Alaska Airlines", "price": 582, "is_nonstop": 1, "duration_mins": 475},
        {"airline": "Korean Air", "price": 648, "is_nonstop": 0, "duration_mins": 530},
    ]),
    ("HND-HNL", "2026-07-15", [
        {"airline": "Alaska Airlines", "price": 557, "is_nonstop": 1, "duration_mins": 475},
        {"airline": "Alaska Airlines", "price": 557, "is_nonstop": 1, "duration_mins": 475},
        {"airline": "Japan Airlines", "price": 594, "is_nonstop": 0, "duration_mins": 510},
    ]),
    ("HND-HNL", "2026-08-01", [
        {"airline": "Korean Air", "price": 761, "is_nonstop": 0, "duration_mins": 530},
        {"airline": "Delta Air Lines", "price": 765, "is_nonstop": 1, "duration_mins": 474},
        {"airline": "Korean Air", "price": 770, "is_nonstop": 0, "duration_mins": 530},
    ]),
    ("HND-HNL", "2026-09-01", [
        {"airline": "Alaska Airlines", "price": 396, "is_nonstop": 1, "duration_mins": 475},
        {"airline": "Alaska Airlines", "price": 396, "is_nonstop": 1, "duration_mins": 475},
        {"airline": "Delta Air Lines", "price": 452, "is_nonstop": 1, "duration_mins": 470},
    ]),
    ("HND-HNL", "2026-11-25", [
        {"airline": "Alaska Airlines", "price": 450, "is_nonstop": 1, "duration_mins": 435},
        {"airline": "Alaska Airlines", "price": 450, "is_nonstop": 1, "duration_mins": 435},
        {"airline": "Delta Air Lines", "price": 452, "is_nonstop": 1, "duration_mins": 445},
    ]),
    ("HND-HNL", "2026-12-20", [
        {"airline": "Alaska Airlines", "price": 450, "is_nonstop": 1, "duration_mins": 435},
        {"airline": "Alaska Airlines", "price": 450, "is_nonstop": 1, "duration_mins": 435},
        {"airline": "Delta Air Lines", "price": 452, "is_nonstop": 1, "duration_mins": 420},
    ]),
    ("HND-HNL", "2027-01-15", [
        {"airline": "Delta Air Lines", "price": 452, "is_nonstop": 1, "duration_mins": 410},
        {"airline": "Korean Air", "price": 586, "is_nonstop": 0, "duration_mins": 490},
        {"airline": "Korean Air", "price": 591, "is_nonstop": 0, "duration_mins": 490},
    ]),

    # KIX-HNL (all 8 returned inline)
    ("KIX-HNL", "2026-06-15", [
        {"airline": "Japan Airlines", "price": 452, "is_nonstop": 0, "duration_mins": 475},
        {"airline": "Japan Airlines", "price": 452, "is_nonstop": 0, "duration_mins": 475},
        {"airline": "Japan Airlines", "price": 452, "is_nonstop": 0, "duration_mins": 475},
    ]),
    ("KIX-HNL", "2026-07-04", [
        {"airline": "Japan Airlines", "price": 591, "is_nonstop": 0, "duration_mins": 475},
        {"airline": "Japan Airlines", "price": 591, "is_nonstop": 0, "duration_mins": 475},
        {"airline": "Japan Airlines", "price": 638, "is_nonstop": 0, "duration_mins": 475},
    ]),
    ("KIX-HNL", "2026-07-15", [
        {"airline": "Alaska Airlines", "price": 611, "is_nonstop": 1, "duration_mins": 510},
        {"airline": "Japan Airlines", "price": 613, "is_nonstop": 0, "duration_mins": 475},
        {"airline": "Japan Airlines", "price": 613, "is_nonstop": 0, "duration_mins": 475},
    ]),
    ("KIX-HNL", "2026-08-01", [
        {"airline": "Korean Air", "price": 763, "is_nonstop": 0, "duration_mins": 530},
        {"airline": "Korean Air", "price": 763, "is_nonstop": 0, "duration_mins": 530},
        {"airline": "All Nippon Airways", "price": 824, "is_nonstop": 0, "duration_mins": 474},
    ]),
    ("KIX-HNL", "2026-09-01", [
        {"airline": "Japan Airlines", "price": 452, "is_nonstop": 0, "duration_mins": 475},
        {"airline": "Japan Airlines", "price": 452, "is_nonstop": 0, "duration_mins": 475},
        {"airline": "Japan Airlines", "price": 452, "is_nonstop": 0, "duration_mins": 475},
    ]),
    ("KIX-HNL", "2026-11-25", [
        {"airline": "Korean Air", "price": 463, "is_nonstop": 0, "duration_mins": 490},
        {"airline": "Korean Air", "price": 463, "is_nonstop": 0, "duration_mins": 490},
        {"airline": "Korean Air", "price": 463, "is_nonstop": 0, "duration_mins": 490},
    ]),
    ("KIX-HNL", "2026-12-20", [
        {"airline": "Japan Airlines", "price": 507, "is_nonstop": 0, "duration_mins": 435},
        {"airline": "Japan Airlines", "price": 507, "is_nonstop": 0, "duration_mins": 435},
        {"airline": "Japan Airlines", "price": 507, "is_nonstop": 0, "duration_mins": 435},
    ]),
    ("KIX-HNL", "2027-01-15", [
        {"airline": "Korean Air", "price": 589, "is_nonstop": 0, "duration_mins": 490},
        {"airline": "Korean Air", "price": 589, "is_nonstop": 0, "duration_mins": 490},
        {"airline": "Korean Air", "price": 589, "is_nonstop": 0, "duration_mins": 490},
    ]),

    # NRT-HNL 2026-08-01 (returned inline)
    ("NRT-HNL", "2026-08-01", [
        {"airline": "Korean Air", "price": 592, "is_nonstop": 0, "duration_mins": 530},
        {"airline": "Korean Air", "price": 592, "is_nonstop": 0, "duration_mins": 530},
        {"airline": "Korean Air", "price": 648, "is_nonstop": 0, "duration_mins": 530},
    ]),

    # ICN-HNL 2026-11-25 and 2027-01-15 (returned inline)
    ("ICN-HNL", "2026-11-25", [
        {"airline": "Perimeter Aviation", "price": 432, "is_nonstop": 1, "duration_mins": 500},
        {"airline": "Korean Air", "price": 479, "is_nonstop": 0, "duration_mins": 490},
        {"airline": "Korean Air", "price": 479, "is_nonstop": 0, "duration_mins": 490},
    ]),
    ("ICN-HNL", "2027-01-15", [
        {"airline": "Perimeter Aviation", "price": 466, "is_nonstop": 1, "duration_mins": 500},
        {"airline": "Korean Air", "price": 603, "is_nonstop": 0, "duration_mins": 490},
        {"airline": "Korean Air", "price": 603, "is_nonstop": 0, "duration_mins": 490},
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
