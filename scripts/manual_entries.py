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

# Manual entries — top 3 cheapest non-ghost fares per (corridor, date), observed today.
MANUAL = [
    # HND-HNL
    ("HND-HNL", "2026-06-15", [
        {"airline": "Delta Air Lines", "price": 460, "is_nonstop": 1, "duration_mins": 460},
        {"airline": "Korean Air", "price": 469, "is_nonstop": 0, "duration_mins": 510},
        {"airline": "Korean Air", "price": 479, "is_nonstop": 0, "duration_mins": 510},
    ]),
    ("HND-HNL", "2026-07-04", [
        {"airline": "Delta Air Lines", "price": 461, "is_nonstop": 1, "duration_mins": 473},
        {"airline": "Alaska Airlines", "price": 593, "is_nonstop": 1, "duration_mins": 475},
        {"airline": "Alaska Airlines", "price": 737, "is_nonstop": 1, "duration_mins": 475},
    ]),
    ("HND-HNL", "2026-07-15", [
        {"airline": "Delta Air Lines", "price": 460, "is_nonstop": 1, "duration_mins": 473},
        {"airline": "Alaska Airlines", "price": 699, "is_nonstop": 1, "duration_mins": 475},
        {"airline": "Alaska Airlines", "price": 699, "is_nonstop": 1, "duration_mins": 475},
    ]),
    ("HND-HNL", "2026-08-01", [
        {"airline": "Delta Air Lines", "price": 780, "is_nonstop": 1, "duration_mins": 474},
        {"airline": "Philippine Airlines", "price": 885, "is_nonstop": 0, "duration_mins": 635},
        {"airline": "Korean Air", "price": 926, "is_nonstop": 0, "duration_mins": 530},
    ]),
    ("HND-HNL", "2026-09-01", [
        {"airline": "Alaska Airlines", "price": 459, "is_nonstop": 1, "duration_mins": 475},
        {"airline": "Alaska Airlines", "price": 459, "is_nonstop": 1, "duration_mins": 475},
        {"airline": "Delta Air Lines", "price": 460, "is_nonstop": 1, "duration_mins": 470},
    ]),
    ("HND-HNL", "2026-11-25", [
        {"airline": "Alaska Airlines", "price": 459, "is_nonstop": 1, "duration_mins": 435},
        {"airline": "Alaska Airlines", "price": 459, "is_nonstop": 1, "duration_mins": 435},
        {"airline": "Delta Air Lines", "price": 460, "is_nonstop": 1, "duration_mins": 445},
    ]),
    ("HND-HNL", "2026-12-20", [
        {"airline": "Alaska Airlines", "price": 459, "is_nonstop": 1, "duration_mins": 435},
        {"airline": "Delta Air Lines", "price": 461, "is_nonstop": 1, "duration_mins": 420},
        {"airline": "Japan Airlines", "price": 519, "is_nonstop": 0, "duration_mins": 455},
    ]),
    ("HND-HNL", "2027-01-15", [
        {"airline": "Delta Air Lines", "price": 460, "is_nonstop": 1, "duration_mins": 410},
        {"airline": "Korean Air", "price": 597, "is_nonstop": 0, "duration_mins": 490},
        {"airline": "Korean Air", "price": 603, "is_nonstop": 0, "duration_mins": 490},
    ]),

    # KIX-HNL
    ("KIX-HNL", "2026-06-15", [
        {"airline": "Korean Air", "price": 472, "is_nonstop": 0, "duration_mins": 510},
        {"airline": "Korean Air", "price": 472, "is_nonstop": 0, "duration_mins": 510},
        {"airline": "Korean Air", "price": 472, "is_nonstop": 0, "duration_mins": 510},
    ]),
    ("KIX-HNL", "2026-07-04", [
        {"airline": "Japan Airlines", "price": 651, "is_nonstop": 0, "duration_mins": 475},
        {"airline": "Japan Airlines", "price": 651, "is_nonstop": 0, "duration_mins": 475},
        {"airline": "All Nippon Airways", "price": 725, "is_nonstop": 0, "duration_mins": 473},
    ]),
    ("KIX-HNL", "2026-07-15", [
        {"airline": "Japan Airlines", "price": 645, "is_nonstop": 0, "duration_mins": 470},
        {"airline": "All Nippon Airways", "price": 738, "is_nonstop": 0, "duration_mins": 473},
        {"airline": "All Nippon Airways", "price": 738, "is_nonstop": 0, "duration_mins": 473},
    ]),
    ("KIX-HNL", "2026-08-01", [
        {"airline": "Korean Air", "price": 724, "is_nonstop": 0, "duration_mins": 530},
        {"airline": "Korean Air", "price": 724, "is_nonstop": 0, "duration_mins": 530},
        {"airline": "Korean Air", "price": 734, "is_nonstop": 0, "duration_mins": 530},
    ]),
    ("KIX-HNL", "2026-09-01", [
        {"airline": "Korean Air", "price": 472, "is_nonstop": 0, "duration_mins": 530},
        {"airline": "Korean Air", "price": 472, "is_nonstop": 0, "duration_mins": 530},
        {"airline": "Korean Air", "price": 472, "is_nonstop": 0, "duration_mins": 530},
    ]),
    ("KIX-HNL", "2026-11-25", [
        {"airline": "Korean Air", "price": 472, "is_nonstop": 0, "duration_mins": 490},
        {"airline": "Korean Air", "price": 472, "is_nonstop": 0, "duration_mins": 490},
        {"airline": "Korean Air", "price": 472, "is_nonstop": 0, "duration_mins": 490},
    ]),
    ("KIX-HNL", "2026-12-20", [
        {"airline": "Japan Airlines", "price": 516, "is_nonstop": 0, "duration_mins": 435},
        {"airline": "Japan Airlines", "price": 516, "is_nonstop": 0, "duration_mins": 435},
        {"airline": "Japan Airlines", "price": 516, "is_nonstop": 0, "duration_mins": 435},
    ]),
    ("KIX-HNL", "2027-01-15", [
        {"airline": "Korean Air", "price": 600, "is_nonstop": 0, "duration_mins": 490},
        {"airline": "Korean Air", "price": 600, "is_nonstop": 0, "duration_mins": 490},
        {"airline": "Korean Air", "price": 600, "is_nonstop": 0, "duration_mins": 490},
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
