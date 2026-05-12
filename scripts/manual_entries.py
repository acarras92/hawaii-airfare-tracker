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
        {"airline": "Delta Air Lines", "price": 458, "is_nonstop": 1, "duration_mins": 460},
        {"airline": "Korean Air", "price": 466, "is_nonstop": 0, "duration_mins": 510},
        {"airline": "Korean Air", "price": 476, "is_nonstop": 0, "duration_mins": 510},
    ]),
    ("HND-HNL", "2026-07-04", [
        {"airline": "Delta Air Lines", "price": 458, "is_nonstop": 1, "duration_mins": 473},
        {"airline": "Alaska Airlines", "price": 593, "is_nonstop": 1, "duration_mins": 475},
        {"airline": "Alaska Airlines", "price": 593, "is_nonstop": 1, "duration_mins": 475},
    ]),
    ("HND-HNL", "2026-07-15", [
        {"airline": "Delta Air Lines", "price": 667, "is_nonstop": 1, "duration_mins": 473},
        {"airline": "Korean Air", "price": 669, "is_nonstop": 0, "duration_mins": 530},
        {"airline": "Alaska Airlines", "price": 698, "is_nonstop": 1, "duration_mins": 475},
    ]),
    ("HND-HNL", "2026-08-01", [
        {"airline": "Korean Air", "price": 771, "is_nonstop": 0, "duration_mins": 530},
        {"airline": "Delta Air Lines", "price": 775, "is_nonstop": 1, "duration_mins": 474},
        {"airline": "Philippine Airlines", "price": 814, "is_nonstop": 0, "duration_mins": 635},
    ]),
    ("HND-HNL", "2026-09-01", [
        {"airline": "Delta Air Lines", "price": 458, "is_nonstop": 1, "duration_mins": 470},
        {"airline": "Alaska Airlines", "price": 459, "is_nonstop": 1, "duration_mins": 475},
        {"airline": "Alaska Airlines", "price": 459, "is_nonstop": 1, "duration_mins": 475},
    ]),
    ("HND-HNL", "2026-11-25", [
        {"airline": "Delta Air Lines", "price": 458, "is_nonstop": 1, "duration_mins": 445},
        {"airline": "Alaska Airlines", "price": 459, "is_nonstop": 1, "duration_mins": 435},
        {"airline": "Alaska Airlines", "price": 459, "is_nonstop": 1, "duration_mins": 435},
    ]),
    ("HND-HNL", "2026-12-20", [
        {"airline": "Delta Air Lines", "price": 458, "is_nonstop": 1, "duration_mins": 420},
        {"airline": "Alaska Airlines", "price": 459, "is_nonstop": 1, "duration_mins": 435},
        {"airline": "Alaska Airlines", "price": 516, "is_nonstop": 0, "duration_mins": 455},
    ]),
    ("HND-HNL", "2027-01-15", [
        {"airline": "Delta Air Lines", "price": 458, "is_nonstop": 1, "duration_mins": 410},
        {"airline": "Asiana Airlines", "price": 594, "is_nonstop": 0, "duration_mins": 490},
        {"airline": "Asiana Airlines", "price": 599, "is_nonstop": 0, "duration_mins": 490},
    ]),

    # KIX-HNL
    ("KIX-HNL", "2026-06-15", [
        {"airline": "Korean Air", "price": 469, "is_nonstop": 0, "duration_mins": 510},
        {"airline": "Korean Air", "price": 469, "is_nonstop": 0, "duration_mins": 510},
        {"airline": "Korean Air", "price": 469, "is_nonstop": 0, "duration_mins": 510},
    ]),
    ("KIX-HNL", "2026-07-04", [
        {"airline": "Alaska Airlines", "price": 624, "is_nonstop": 0, "duration_mins": 475},
        {"airline": "Alaska Airlines", "price": 647, "is_nonstop": 0, "duration_mins": 475},
        {"airline": "Alaska Airlines", "price": 647, "is_nonstop": 0, "duration_mins": 475},
    ]),
    ("KIX-HNL", "2026-07-15", [
        {"airline": "Korean Air", "price": 672, "is_nonstop": 0, "duration_mins": 530},
        {"airline": "Korean Air", "price": 672, "is_nonstop": 0, "duration_mins": 530},
        {"airline": "Korean Air", "price": 672, "is_nonstop": 0, "duration_mins": 530},
    ]),
    ("KIX-HNL", "2026-08-01", [
        {"airline": "Korean Air", "price": 720, "is_nonstop": 0, "duration_mins": 530},
        {"airline": "Korean Air", "price": 720, "is_nonstop": 0, "duration_mins": 530},
        {"airline": "Korean Air", "price": 720, "is_nonstop": 0, "duration_mins": 530},
    ]),
    ("KIX-HNL", "2026-09-01", [
        {"airline": "Korean Air", "price": 469, "is_nonstop": 0, "duration_mins": 530},
        {"airline": "Korean Air", "price": 469, "is_nonstop": 0, "duration_mins": 530},
        {"airline": "Korean Air", "price": 469, "is_nonstop": 0, "duration_mins": 530},
    ]),
    ("KIX-HNL", "2026-11-25", [
        {"airline": "Korean Air", "price": 469, "is_nonstop": 0, "duration_mins": 490},
        {"airline": "Korean Air", "price": 469, "is_nonstop": 0, "duration_mins": 490},
        {"airline": "Korean Air", "price": 469, "is_nonstop": 0, "duration_mins": 490},
    ]),
    ("KIX-HNL", "2026-12-20", [
        {"airline": "Alaska Airlines", "price": 513, "is_nonstop": 0, "duration_mins": 435},
        {"airline": "Alaska Airlines", "price": 513, "is_nonstop": 0, "duration_mins": 435},
        {"airline": "Alaska Airlines", "price": 513, "is_nonstop": 0, "duration_mins": 435},
    ]),
    ("KIX-HNL", "2027-01-15", [
        {"airline": "Asiana Airlines", "price": 597, "is_nonstop": 0, "duration_mins": 490},
        {"airline": "Asiana Airlines", "price": 597, "is_nonstop": 0, "duration_mins": 490},
        {"airline": "Asiana Airlines", "price": 597, "is_nonstop": 0, "duration_mins": 490},
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
