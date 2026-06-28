#!/usr/bin/env python3
"""Merge manually-extracted top-3 fares for inline-response corridors into mcp_flights.json.

These corridors (HND, KIX, ICN origin, plus some NRT dates) often return small
inline responses that do NOT get saved to the session's tool-results dir, so they
need manual population. Duration values mirror the trans-Pacific leg duration the
aggregator would emit (last-leg duration for connections, single-leg for nonstops)
to stay consistent with the rest of the dataset.

Refreshed 2026-06-28. The flight-search MCP was UP this session and returned full
fares for every corridor. HND and KIX produced ZERO files in any session (always
inline), so every live HND/KIX combo MUST be overlaid here or it is dropped --
the aggregator reported all 16 HND/KIX combos missing. NRT 07-04/07-15/08-01 and
ICN 07-04/07-15/08-01/09-01/12-20 came inline today and are overlaid with fresh
values (the aggregator otherwise backfills them from stale prior-session files).
NRT 09-01/11-25/12-20/01-15 and ICN 11-25/01-15 saved to files this session and
are NOT listed here (the overlay would clobber fresh file data). 2026-06-15 is in
the past (today is 2026-06-28) and is omitted entirely.
"""
import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "data" / "mcp_flights.json"

# Manual entries -- top 3 cheapest non-ghost fares per (corridor, date), observed 2026-06-28.
MANUAL = [
    # NRT-HNL (only 07-04 / 07-15 / 08-01 came inline; later NRT dates are file-based this session)
    ("NRT-HNL", "2026-07-04", [
        {"airline": "Korean Air", "price": 430, "is_nonstop": 0, "duration_mins": 530},
        {"airline": "Korean Air", "price": 430, "is_nonstop": 0, "duration_mins": 530},
        {"airline": "Korean Air", "price": 430, "is_nonstop": 0, "duration_mins": 530},
    ]),
    ("NRT-HNL", "2026-07-15", [
        {"airline": "Korean Air", "price": 430, "is_nonstop": 0, "duration_mins": 530},
        {"airline": "Korean Air", "price": 430, "is_nonstop": 0, "duration_mins": 530},
        {"airline": "Korean Air", "price": 430, "is_nonstop": 0, "duration_mins": 530},
    ]),
    ("NRT-HNL", "2026-08-01", [
        {"airline": "Korean Air", "price": 456, "is_nonstop": 0, "duration_mins": 530},
        {"airline": "Korean Air", "price": 585, "is_nonstop": 0, "duration_mins": 530},
        {"airline": "Korean Air", "price": 641, "is_nonstop": 0, "duration_mins": 530},
    ]),

    # HND-HNL (all 7 live dates overlaid -- entirely missing from aggregator)
    ("HND-HNL", "2026-07-04", [
        {"airline": "Alaska Airlines", "price": 345, "is_nonstop": 1, "duration_mins": 475},
        {"airline": "Alaska Airlines", "price": 345, "is_nonstop": 1, "duration_mins": 475},
        {"airline": "Japan Airlines", "price": 403, "is_nonstop": 0, "duration_mins": 510},
    ]),
    ("HND-HNL", "2026-07-15", [
        {"airline": "Alaska Airlines", "price": 345, "is_nonstop": 1, "duration_mins": 475},
        {"airline": "Japan Airlines", "price": 403, "is_nonstop": 0, "duration_mins": 510},
        {"airline": "Japan Airlines", "price": 403, "is_nonstop": 0, "duration_mins": 510},
    ]),
    ("HND-HNL", "2026-08-01", [
        {"airline": "Japan Airlines", "price": 514, "is_nonstop": 0, "duration_mins": 510},
        {"airline": "Japan Airlines", "price": 514, "is_nonstop": 0, "duration_mins": 510},
        {"airline": "Japan Airlines", "price": 514, "is_nonstop": 0, "duration_mins": 510},
    ]),
    ("HND-HNL", "2026-09-01", [
        {"airline": "Philippine Airlines", "price": 417, "is_nonstop": 0, "duration_mins": 635},
        {"airline": "Alaska Airlines", "price": 445, "is_nonstop": 1, "duration_mins": 475},
        {"airline": "Alaska Airlines", "price": 445, "is_nonstop": 1, "duration_mins": 475},
    ]),
    ("HND-HNL", "2026-11-25", [
        {"airline": "Alaska Airlines", "price": 445, "is_nonstop": 1, "duration_mins": 435},
        {"airline": "Alaska Airlines", "price": 445, "is_nonstop": 1, "duration_mins": 435},
        {"airline": "Delta Air Lines", "price": 447, "is_nonstop": 1, "duration_mins": 445},
    ]),
    ("HND-HNL", "2026-12-20", [
        {"airline": "Alaska Airlines", "price": 445, "is_nonstop": 1, "duration_mins": 435},
        {"airline": "Alaska Airlines", "price": 445, "is_nonstop": 1, "duration_mins": 435},
        {"airline": "Delta Air Lines", "price": 448, "is_nonstop": 1, "duration_mins": 420},
    ]),
    ("HND-HNL", "2027-01-15", [
        {"airline": "Delta Air Lines", "price": 447, "is_nonstop": 1, "duration_mins": 410},
        {"airline": "Korean Air", "price": 580, "is_nonstop": 0, "duration_mins": 490},
        {"airline": "Korean Air", "price": 584, "is_nonstop": 0, "duration_mins": 490},
    ]),

    # KIX-HNL (all 7 live dates overlaid -- entirely missing from aggregator)
    ("KIX-HNL", "2026-07-04", [
        {"airline": "Japan Airlines", "price": 400, "is_nonstop": 0, "duration_mins": 475},
        {"airline": "Japan Airlines", "price": 400, "is_nonstop": 0, "duration_mins": 475},
        {"airline": "Japan Airlines", "price": 400, "is_nonstop": 0, "duration_mins": 475},
    ]),
    ("KIX-HNL", "2026-07-15", [
        {"airline": "Japan Airlines", "price": 400, "is_nonstop": 0, "duration_mins": 475},
        {"airline": "Japan Airlines", "price": 400, "is_nonstop": 0, "duration_mins": 475},
        {"airline": "Japan Airlines", "price": 400, "is_nonstop": 0, "duration_mins": 475},
    ]),
    ("KIX-HNL", "2026-08-01", [
        {"airline": "Alaska Airlines", "price": 534, "is_nonstop": 1, "duration_mins": 510},
        {"airline": "Japan Airlines", "price": 825, "is_nonstop": 0, "duration_mins": 475},
        {"airline": "Japan Airlines", "price": 825, "is_nonstop": 0, "duration_mins": 475},
    ]),
    ("KIX-HNL", "2026-09-01", [
        {"airline": "Korean Air", "price": 458, "is_nonstop": 0, "duration_mins": 530},
        {"airline": "Korean Air", "price": 458, "is_nonstop": 0, "duration_mins": 530},
        {"airline": "Korean Air", "price": 458, "is_nonstop": 0, "duration_mins": 530},
    ]),
    ("KIX-HNL", "2026-11-25", [
        {"airline": "Korean Air", "price": 458, "is_nonstop": 0, "duration_mins": 490},
        {"airline": "Korean Air", "price": 458, "is_nonstop": 0, "duration_mins": 490},
        {"airline": "Korean Air", "price": 458, "is_nonstop": 0, "duration_mins": 490},
    ]),
    ("KIX-HNL", "2026-12-20", [
        {"airline": "Japan Airlines", "price": 501, "is_nonstop": 0, "duration_mins": 435},
        {"airline": "Japan Airlines", "price": 501, "is_nonstop": 0, "duration_mins": 435},
        {"airline": "Japan Airlines", "price": 501, "is_nonstop": 0, "duration_mins": 435},
    ]),
    ("KIX-HNL", "2027-01-15", [
        {"airline": "Korean Air", "price": 582, "is_nonstop": 0, "duration_mins": 490},
        {"airline": "Korean Air", "price": 582, "is_nonstop": 0, "duration_mins": 490},
        {"airline": "Korean Air", "price": 582, "is_nonstop": 0, "duration_mins": 490},
    ]),

    # ICN-HNL (07-04 / 07-15 / 08-01 / 09-01 / 12-20 came inline; 11-25 / 01-15 are file-based this session)
    ("ICN-HNL", "2026-07-04", [
        {"airline": "Korean Air", "price": 536, "is_nonstop": 0, "duration_mins": 510},
        {"airline": "Korean Air", "price": 591, "is_nonstop": 0, "duration_mins": 510},
        {"airline": "Korean Air", "price": 695, "is_nonstop": 0, "duration_mins": 475},
    ]),
    ("ICN-HNL", "2026-07-15", [
        {"airline": "Perimeter Aviation", "price": 446, "is_nonstop": 1, "duration_mins": 530},
        {"airline": "Korean Air", "price": 546, "is_nonstop": 0, "duration_mins": 510},
        {"airline": "Asiana Airlines", "price": 558, "is_nonstop": 0, "duration_mins": 475},
    ]),
    ("ICN-HNL", "2026-08-01", [
        {"airline": "Korean Air", "price": 683, "is_nonstop": 0, "duration_mins": 510},
        {"airline": "Korean Air", "price": 695, "is_nonstop": 0, "duration_mins": 475},
        {"airline": "Korean Air", "price": 695, "is_nonstop": 0, "duration_mins": 475},
    ]),
    ("ICN-HNL", "2026-09-01", [
        {"airline": "Korean Air", "price": 409, "is_nonstop": 0, "duration_mins": 500},
        {"airline": "Korean Air", "price": 409, "is_nonstop": 0, "duration_mins": 500},
        {"airline": "Korean Air", "price": 426, "is_nonstop": 0, "duration_mins": 500},
    ]),
    ("ICN-HNL", "2026-12-20", [
        {"airline": "Korean Air", "price": 546, "is_nonstop": 0, "duration_mins": 455},
        {"airline": "Korean Air", "price": 558, "is_nonstop": 0, "duration_mins": 435},
        {"airline": "Korean Air", "price": 558, "is_nonstop": 0, "duration_mins": 435},
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
