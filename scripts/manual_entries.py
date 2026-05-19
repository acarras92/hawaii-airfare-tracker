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
        {"airline": "Delta Air Lines", "price": 560, "is_nonstop": 1, "duration_mins": 460},
        {"airline": "Korean Air", "price": 569, "is_nonstop": 0, "duration_mins": 525},
        {"airline": "Korean Air", "price": 569, "is_nonstop": 0, "duration_mins": 525},
    ]),
    ("HND-HNL", "2026-07-04", [
        {"airline": "Delta Air Lines", "price": 454, "is_nonstop": 1, "duration_mins": 473},
        {"airline": "Korean Air", "price": 657, "is_nonstop": 0, "duration_mins": 530},
        {"airline": "Asiana Airlines", "price": 662, "is_nonstop": 0, "duration_mins": 530},
    ]),
    ("HND-HNL", "2026-07-15", [
        {"airline": "Alaska Airlines", "price": 561, "is_nonstop": 1, "duration_mins": 475},
        {"airline": "Japan Airlines", "price": 655, "is_nonstop": 1, "duration_mins": 460},
        {"airline": "Japan Airlines", "price": 655, "is_nonstop": 1, "duration_mins": 460},
    ]),
    ("HND-HNL", "2026-08-01", [
        {"airline": "Japan Airlines", "price": 761, "is_nonstop": 0, "duration_mins": 460},
        {"airline": "Delta Air Lines", "price": 768, "is_nonstop": 1, "duration_mins": 474},
        {"airline": "Korean Air", "price": 770, "is_nonstop": 0, "duration_mins": 530},
    ]),
    ("HND-HNL", "2026-09-01", [
        {"airline": "Delta Air Lines", "price": 454, "is_nonstop": 1, "duration_mins": 470},
        {"airline": "Alaska Airlines", "price": 454, "is_nonstop": 1, "duration_mins": 475},
        {"airline": "Alaska Airlines", "price": 454, "is_nonstop": 1, "duration_mins": 475},
    ]),
    ("HND-HNL", "2026-11-25", [
        {"airline": "Delta Air Lines", "price": 454, "is_nonstop": 1, "duration_mins": 445},
        {"airline": "Alaska Airlines", "price": 454, "is_nonstop": 1, "duration_mins": 435},
        {"airline": "Alaska Airlines", "price": 454, "is_nonstop": 1, "duration_mins": 435},
    ]),
    ("HND-HNL", "2026-12-20", [
        {"airline": "Japan Airlines", "price": 411, "is_nonstop": 1, "duration_mins": 405},
        {"airline": "Delta Air Lines", "price": 454, "is_nonstop": 1, "duration_mins": 420},
        {"airline": "Japan Airlines", "price": 479, "is_nonstop": 1, "duration_mins": 405},
    ]),
    ("HND-HNL", "2027-01-15", [
        {"airline": "Japan Airlines", "price": 411, "is_nonstop": 1, "duration_mins": 405},
        {"airline": "Delta Air Lines", "price": 454, "is_nonstop": 1, "duration_mins": 410},
        {"airline": "Japan Airlines", "price": 523, "is_nonstop": 1, "duration_mins": 405},
    ]),

    # KIX-HNL
    ("KIX-HNL", "2026-06-15", [
        {"airline": "Korean Air", "price": 562, "is_nonstop": 0, "duration_mins": 525},
        {"airline": "Korean Air", "price": 572, "is_nonstop": 0, "duration_mins": 510},
        {"airline": "Korean Air", "price": 572, "is_nonstop": 0, "duration_mins": 510},
    ]),
    ("KIX-HNL", "2026-07-04", [
        {"airline": "Korean Air", "price": 471, "is_nonstop": 0, "duration_mins": 530},
        {"airline": "Japan Airlines", "price": 616, "is_nonstop": 0, "duration_mins": 475},
        {"airline": "Korean Air", "price": 654, "is_nonstop": 0, "duration_mins": 530},
    ]),
    ("KIX-HNL", "2026-07-15", [
        {"airline": "Asiana Airlines", "price": 552, "is_nonstop": 0, "duration_mins": 530},
        {"airline": "Japan Airlines", "price": 616, "is_nonstop": 0, "duration_mins": 475},
        {"airline": "Japan Airlines", "price": 617, "is_nonstop": 0, "duration_mins": 475},
    ]),
    ("KIX-HNL", "2026-08-01", [
        {"airline": "Asiana Airlines", "price": 716, "is_nonstop": 0, "duration_mins": 530},
        {"airline": "Asiana Airlines", "price": 716, "is_nonstop": 0, "duration_mins": 530},
        {"airline": "Korean Air", "price": 719, "is_nonstop": 0, "duration_mins": 530},
    ]),
    ("KIX-HNL", "2026-09-01", [
        {"airline": "Korean Air", "price": 465, "is_nonstop": 0, "duration_mins": 530},
        {"airline": "Korean Air", "price": 465, "is_nonstop": 0, "duration_mins": 530},
        {"airline": "Korean Air", "price": 465, "is_nonstop": 0, "duration_mins": 530},
    ]),
    ("KIX-HNL", "2026-11-25", [
        {"airline": "Japan Airlines", "price": 417, "is_nonstop": 0, "duration_mins": 420},
        {"airline": "Japan Airlines", "price": 419, "is_nonstop": 0, "duration_mins": 425},
        {"airline": "Japan Airlines", "price": 419, "is_nonstop": 0, "duration_mins": 425},
    ]),
    ("KIX-HNL", "2026-12-20", [
        {"airline": "Japan Airlines", "price": 417, "is_nonstop": 0, "duration_mins": 405},
        {"airline": "Japan Airlines", "price": 418, "is_nonstop": 0, "duration_mins": 405},
        {"airline": "Japan Airlines", "price": 486, "is_nonstop": 0, "duration_mins": 405},
    ]),
    ("KIX-HNL", "2027-01-15", [
        {"airline": "Japan Airlines", "price": 417, "is_nonstop": 0, "duration_mins": 405},
        {"airline": "Japan Airlines", "price": 417, "is_nonstop": 0, "duration_mins": 405},
        {"airline": "Japan Airlines", "price": 418, "is_nonstop": 0, "duration_mins": 405},
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
