#!/usr/bin/env python3
"""Merge manually-extracted top-3 fares for inline-response corridors into mcp_flights.json.

These corridors (HND, KIX, ICN origin, plus some NRT dates) often return small
inline responses that do NOT get saved to the session's tool-results dir, so they
need manual population. Duration values mirror the trans-Pacific leg duration the
aggregator would emit (last-leg duration for connections, single-leg for nonstops)
to stay consistent with the rest of the dataset.

Refreshed 2026-06-30. The flight-search MCP was UP this session and returned full
fares for every corridor. HND and KIX produced ZERO files in any session (always
inline), so every live HND/KIX combo MUST be overlaid here or it is dropped.
NRT 07-04/07-15/08-01 and ICN 07-15/08-01/09-01/11-25 came inline today and are
overlaid with fresh values (the aggregator otherwise backfills them from stale
prior-session files). NRT 07-15 only returned fares on its 3rd attempt (empty on
the first two). NRT 09-01/11-25/12-20/01-15 and ICN 07-04/12-20/01-15 saved to
files this session and are NOT listed here (the overlay would clobber fresh file
data). 2026-06-15 is in the past (today is 2026-06-30) and is omitted entirely.
"""
import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "data" / "mcp_flights.json"

# Manual entries -- top 3 cheapest non-ghost fares per (corridor, date), observed 2026-06-30.
MANUAL = [
    # NRT-HNL (07-04 / 07-15 / 08-01 came inline; 09-01 / 11-25 / 12-20 / 01-15 are file-based this session.
    # 07-15 only returned fares on its 3rd attempt -- empty on the first two, so it is overlaid here.)
    ("NRT-HNL", "2026-07-04", [
        {"airline": "Korean Air", "price": 429, "is_nonstop": 0, "duration_mins": 530},
        {"airline": "Korean Air", "price": 429, "is_nonstop": 0, "duration_mins": 530},
        {"airline": "Korean Air", "price": 429, "is_nonstop": 0, "duration_mins": 530},
    ]),
    ("NRT-HNL", "2026-07-15", [
        {"airline": "Korean Air", "price": 429, "is_nonstop": 0, "duration_mins": 530},
        {"airline": "Korean Air", "price": 429, "is_nonstop": 0, "duration_mins": 530},
        {"airline": "Korean Air", "price": 429, "is_nonstop": 0, "duration_mins": 530},
    ]),
    ("NRT-HNL", "2026-08-01", [
        {"airline": "Korean Air", "price": 454, "is_nonstop": 0, "duration_mins": 530},
        {"airline": "Korean Air", "price": 750, "is_nonstop": 0, "duration_mins": 530},
        {"airline": "Korean Air", "price": 750, "is_nonstop": 0, "duration_mins": 530},
    ]),

    # HND-HNL (all 7 live dates overlaid -- entirely missing from aggregator)
    ("HND-HNL", "2026-07-04", [
        {"airline": "Delta Air Lines", "price": 345, "is_nonstop": 1, "duration_mins": 473},
        {"airline": "Alaska Airlines", "price": 345, "is_nonstop": 1, "duration_mins": 475},
        {"airline": "Alaska Airlines", "price": 345, "is_nonstop": 1, "duration_mins": 475},
    ]),
    ("HND-HNL", "2026-07-15", [
        {"airline": "Korean Air", "price": 486, "is_nonstop": 0, "duration_mins": 530},
        {"airline": "Alaska Airlines", "price": 551, "is_nonstop": 1, "duration_mins": 475},
        {"airline": "Alaska Airlines", "price": 551, "is_nonstop": 1, "duration_mins": 475},
    ]),
    ("HND-HNL", "2026-08-01", [
        {"airline": "Japan Airlines", "price": 512, "is_nonstop": 0, "duration_mins": 510},
        {"airline": "Japan Airlines", "price": 512, "is_nonstop": 0, "duration_mins": 510},
        {"airline": "Japan Airlines", "price": 512, "is_nonstop": 0, "duration_mins": 510},
    ]),
    ("HND-HNL", "2026-09-01", [
        {"airline": "Philippine Airlines", "price": 415, "is_nonstop": 0, "duration_mins": 635},
        {"airline": "Alaska Airlines", "price": 445, "is_nonstop": 1, "duration_mins": 475},
        {"airline": "Alaska Airlines", "price": 445, "is_nonstop": 1, "duration_mins": 475},
    ]),
    ("HND-HNL", "2026-11-25", [
        {"airline": "Alaska Airlines", "price": 445, "is_nonstop": 1, "duration_mins": 435},
        {"airline": "Alaska Airlines", "price": 445, "is_nonstop": 1, "duration_mins": 435},
        {"airline": "Delta Air Lines", "price": 446, "is_nonstop": 1, "duration_mins": 445},
    ]),
    ("HND-HNL", "2026-12-20", [
        {"airline": "Alaska Airlines", "price": 445, "is_nonstop": 1, "duration_mins": 435},
        {"airline": "Alaska Airlines", "price": 445, "is_nonstop": 1, "duration_mins": 435},
        {"airline": "Delta Air Lines", "price": 446, "is_nonstop": 1, "duration_mins": 420},
    ]),
    ("HND-HNL", "2027-01-15", [
        {"airline": "Delta Air Lines", "price": 446, "is_nonstop": 1, "duration_mins": 410},
        {"airline": "Korean Air", "price": 578, "is_nonstop": 0, "duration_mins": 490},
        {"airline": "Korean Air", "price": 583, "is_nonstop": 0, "duration_mins": 490},
    ]),

    # KIX-HNL (all 7 live dates overlaid -- entirely missing from aggregator)
    ("KIX-HNL", "2026-07-04", [
        {"airline": "Japan Airlines", "price": 399, "is_nonstop": 0, "duration_mins": 475},
        {"airline": "Japan Airlines", "price": 399, "is_nonstop": 0, "duration_mins": 475},
        {"airline": "Korean Air", "price": 431, "is_nonstop": 0, "duration_mins": 530},
    ]),
    ("KIX-HNL", "2026-07-15", [
        {"airline": "Japan Airlines", "price": 399, "is_nonstop": 0, "duration_mins": 475},
        {"airline": "Korean Air", "price": 431, "is_nonstop": 0, "duration_mins": 530},
        {"airline": "Korean Air", "price": 431, "is_nonstop": 0, "duration_mins": 530},
    ]),
    ("KIX-HNL", "2026-08-01", [
        {"airline": "Alaska Airlines", "price": 534, "is_nonstop": 1, "duration_mins": 510},
        {"airline": "Japan Airlines", "price": 836, "is_nonstop": 1, "duration_mins": 480},
        {"airline": "Japan Airlines", "price": 863, "is_nonstop": 0, "duration_mins": 475},
    ]),
    ("KIX-HNL", "2026-09-01", [
        {"airline": "Korean Air", "price": 457, "is_nonstop": 0, "duration_mins": 530},
        {"airline": "Korean Air", "price": 457, "is_nonstop": 0, "duration_mins": 530},
        {"airline": "Korean Air", "price": 457, "is_nonstop": 0, "duration_mins": 530},
    ]),
    ("KIX-HNL", "2026-11-25", [
        {"airline": "Korean Air", "price": 457, "is_nonstop": 0, "duration_mins": 490},
        {"airline": "Korean Air", "price": 457, "is_nonstop": 0, "duration_mins": 490},
        {"airline": "Korean Air", "price": 457, "is_nonstop": 0, "duration_mins": 490},
    ]),
    ("KIX-HNL", "2026-12-20", [
        {"airline": "Japan Airlines", "price": 500, "is_nonstop": 0, "duration_mins": 435},
        {"airline": "Japan Airlines", "price": 500, "is_nonstop": 0, "duration_mins": 435},
        {"airline": "Japan Airlines", "price": 500, "is_nonstop": 0, "duration_mins": 435},
    ]),
    ("KIX-HNL", "2027-01-15", [
        {"airline": "Korean Air", "price": 580, "is_nonstop": 0, "duration_mins": 490},
        {"airline": "Korean Air", "price": 580, "is_nonstop": 0, "duration_mins": 490},
        {"airline": "Korean Air", "price": 580, "is_nonstop": 0, "duration_mins": 490},
    ]),

    # ICN-HNL (07-15 / 08-01 / 09-01 / 11-25 came inline; 07-04 / 12-20 / 01-15 are file-based this session)
    ("ICN-HNL", "2026-07-15", [
        {"airline": "Perimeter Aviation", "price": 442, "is_nonstop": 1, "duration_mins": 530},
        {"airline": "Korean Air", "price": 469, "is_nonstop": 0, "duration_mins": 510},
        {"airline": "Asiana Airlines", "price": 481, "is_nonstop": 0, "duration_mins": 475},
    ]),
    ("ICN-HNL", "2026-08-01", [
        {"airline": "Korean Air", "price": 675, "is_nonstop": 0, "duration_mins": 510},
        {"airline": "Korean Air", "price": 687, "is_nonstop": 0, "duration_mins": 475},
        {"airline": "Korean Air", "price": 687, "is_nonstop": 0, "duration_mins": 475},
    ]),
    ("ICN-HNL", "2026-09-01", [
        {"airline": "Korean Air", "price": 404, "is_nonstop": 0, "duration_mins": 500},
        {"airline": "Korean Air", "price": 404, "is_nonstop": 0, "duration_mins": 500},
        {"airline": "Asiana Airlines", "price": 407, "is_nonstop": 0, "duration_mins": 475},
    ]),
    ("ICN-HNL", "2026-11-25", [
        {"airline": "Korean Air", "price": 462, "is_nonstop": 0, "duration_mins": 455},
        {"airline": "Korean Air", "price": 462, "is_nonstop": 0, "duration_mins": 455},
        {"airline": "Korean Air", "price": 475, "is_nonstop": 0, "duration_mins": 435},
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
