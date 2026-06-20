#!/usr/bin/env python3
"""Merge manually-extracted top-3 fares for inline-response corridors into mcp_flights.json.

These corridors (HND, KIX, ICN origin, plus some NRT dates) often return small
inline responses that do NOT get saved to the session's tool-results dir, so they
need manual population. Duration values mirror the trans-Pacific leg duration the
aggregator would emit (last-leg duration for connections, single-leg for nonstops)
to stay consistent with the rest of the dataset.

Refreshed 2026-06-20. Today the inline combos were: all HND, all KIX, ICN-HNL for
07-04/07-15/08-01/09-01/11-25/01-15, and NRT-HNL for 07-04/07-15/08-01. The other
NRT dates (09-01/11-25/12-20/01-15) and ICN-HNL 12-20 saved to files this session
and are picked up by the aggregator directly -- do NOT add them here or this overlay
would clobber fresh file data. 2026-06-15 is in the past (today is 2026-06-20) and
is omitted entirely. The aggregator silently BACKFILLS inline combos from stale
prior-session files, so they MUST be overlaid here with today's fresh top-3.
"""
import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "data" / "mcp_flights.json"

# Manual entries -- top 3 cheapest non-ghost fares per (corridor, date), observed 2026-06-20.
MANUAL = [
    # NRT-HNL (only 07-04 / 07-15 / 08-01 came inline; other NRT dates are file-based)
    ("NRT-HNL", "2026-07-04", [
        {"airline": "Korean Air", "price": 431, "is_nonstop": 0, "duration_mins": 530},
        {"airline": "Korean Air", "price": 431, "is_nonstop": 0, "duration_mins": 530},
        {"airline": "Korean Air", "price": 431, "is_nonstop": 0, "duration_mins": 530},
    ]),
    ("NRT-HNL", "2026-07-15", [
        {"airline": "Korean Air", "price": 431, "is_nonstop": 0, "duration_mins": 530},
        {"airline": "Korean Air", "price": 431, "is_nonstop": 0, "duration_mins": 530},
        {"airline": "Korean Air", "price": 431, "is_nonstop": 0, "duration_mins": 530},
    ]),
    ("NRT-HNL", "2026-08-01", [
        {"airline": "Korean Air", "price": 457, "is_nonstop": 0, "duration_mins": 530},
        {"airline": "Korean Air", "price": 754, "is_nonstop": 0, "duration_mins": 530},
        {"airline": "Korean Air", "price": 754, "is_nonstop": 0, "duration_mins": 530},
    ]),

    # HND-HNL (all 7 returned inline)
    ("HND-HNL", "2026-07-04", [
        {"airline": "Alaska Airlines", "price": 603, "is_nonstop": 1, "duration_mins": 475},
        {"airline": "Alaska Airlines", "price": 603, "is_nonstop": 1, "duration_mins": 475},
        {"airline": "Korean Air", "price": 611, "is_nonstop": 0, "duration_mins": 530},
    ]),
    ("HND-HNL", "2026-07-15", [
        {"airline": "Alaska Airlines", "price": 346, "is_nonstop": 1, "duration_mins": 475},
        {"airline": "Alaska Airlines", "price": 346, "is_nonstop": 1, "duration_mins": 475},
        {"airline": "Korean Air", "price": 489, "is_nonstop": 0, "duration_mins": 530},
    ]),
    ("HND-HNL", "2026-08-01", [
        {"airline": "Delta Air Lines", "price": 770, "is_nonstop": 1, "duration_mins": 474},
        {"airline": "Alaska Airlines", "price": 811, "is_nonstop": 1, "duration_mins": 475},
        {"airline": "Alaska Airlines", "price": 811, "is_nonstop": 1, "duration_mins": 475},
    ]),
    ("HND-HNL", "2026-09-01", [
        {"airline": "Alaska Airlines", "price": 346, "is_nonstop": 1, "duration_mins": 475},
        {"airline": "Delta Air Lines", "price": 448, "is_nonstop": 1, "duration_mins": 470},
        {"airline": "Korean Air", "price": 456, "is_nonstop": 0, "duration_mins": 530},
    ]),
    ("HND-HNL", "2026-11-25", [
        {"airline": "Alaska Airlines", "price": 447, "is_nonstop": 1, "duration_mins": 435},
        {"airline": "Alaska Airlines", "price": 447, "is_nonstop": 1, "duration_mins": 435},
        {"airline": "Delta Air Lines", "price": 448, "is_nonstop": 1, "duration_mins": 445},
    ]),
    ("HND-HNL", "2026-12-20", [
        {"airline": "Alaska Airlines", "price": 447, "is_nonstop": 1, "duration_mins": 435},
        {"airline": "Alaska Airlines", "price": 447, "is_nonstop": 1, "duration_mins": 435},
        {"airline": "Delta Air Lines", "price": 449, "is_nonstop": 1, "duration_mins": 420},
    ]),
    ("HND-HNL", "2027-01-15", [
        {"airline": "Delta Air Lines", "price": 448, "is_nonstop": 1, "duration_mins": 410},
        {"airline": "Korean Air", "price": 549, "is_nonstop": 0, "duration_mins": 460},
        {"airline": "Korean Air", "price": 567, "is_nonstop": 0, "duration_mins": 490},
    ]),

    # KIX-HNL (all 7 returned inline)
    ("KIX-HNL", "2026-07-04", [
        {"airline": "Japan Airlines", "price": 403, "is_nonstop": 0, "duration_mins": 475},
        {"airline": "Japan Airlines", "price": 403, "is_nonstop": 0, "duration_mins": 475},
        {"airline": "Korean Air", "price": 434, "is_nonstop": 0, "duration_mins": 530},
    ]),
    ("KIX-HNL", "2026-07-15", [
        {"airline": "Japan Airlines", "price": 401, "is_nonstop": 0, "duration_mins": 475},
        {"airline": "Japan Airlines", "price": 401, "is_nonstop": 0, "duration_mins": 475},
        {"airline": "Japan Airlines", "price": 401, "is_nonstop": 0, "duration_mins": 475},
    ]),
    ("KIX-HNL", "2026-08-01", [
        {"airline": "All Nippon Airways", "price": 829, "is_nonstop": 0, "duration_mins": 474},
        {"airline": "All Nippon Airways", "price": 829, "is_nonstop": 0, "duration_mins": 474},
        {"airline": "All Nippon Airways", "price": 829, "is_nonstop": 0, "duration_mins": 474},
    ]),
    ("KIX-HNL", "2026-09-01", [
        {"airline": "Japan Airlines", "price": 401, "is_nonstop": 0, "duration_mins": 475},
        {"airline": "Japan Airlines", "price": 401, "is_nonstop": 0, "duration_mins": 475},
        {"airline": "Japan Airlines", "price": 401, "is_nonstop": 0, "duration_mins": 475},
    ]),
    ("KIX-HNL", "2026-11-25", [
        {"airline": "Korean Air", "price": 459, "is_nonstop": 0, "duration_mins": 490},
        {"airline": "Korean Air", "price": 459, "is_nonstop": 0, "duration_mins": 490},
        {"airline": "Korean Air", "price": 459, "is_nonstop": 0, "duration_mins": 490},
    ]),
    ("KIX-HNL", "2026-12-20", [
        {"airline": "Japan Airlines", "price": 502, "is_nonstop": 0, "duration_mins": 435},
        {"airline": "Japan Airlines", "price": 502, "is_nonstop": 0, "duration_mins": 435},
        {"airline": "Japan Airlines", "price": 502, "is_nonstop": 0, "duration_mins": 435},
    ]),
    ("KIX-HNL", "2027-01-15", [
        {"airline": "Korean Air", "price": 584, "is_nonstop": 0, "duration_mins": 490},
        {"airline": "Korean Air", "price": 584, "is_nonstop": 0, "duration_mins": 490},
        {"airline": "Korean Air", "price": 584, "is_nonstop": 0, "duration_mins": 490},
    ]),

    # ICN-HNL (6 inline; 12-20 saved to a file this session)
    ("ICN-HNL", "2026-07-04", [
        {"airline": "Korean Air", "price": 533, "is_nonstop": 0, "duration_mins": 475},
        {"airline": "Korean Air", "price": 533, "is_nonstop": 0, "duration_mins": 475},
        {"airline": "Korean Air", "price": 533, "is_nonstop": 0, "duration_mins": 475},
    ]),
    ("ICN-HNL", "2026-07-15", [
        {"airline": "Perimeter Aviation", "price": 513, "is_nonstop": 1, "duration_mins": 530},
        {"airline": "Korean Air", "price": 547, "is_nonstop": 0, "duration_mins": 510},
        {"airline": "Korean Air", "price": 560, "is_nonstop": 0, "duration_mins": 475},
    ]),
    ("ICN-HNL", "2026-08-01", [
        {"airline": "Korean Air", "price": 684, "is_nonstop": 0, "duration_mins": 510},
        {"airline": "Korean Air", "price": 697, "is_nonstop": 0, "duration_mins": 475},
        {"airline": "Korean Air", "price": 697, "is_nonstop": 0, "duration_mins": 475},
    ]),
    ("ICN-HNL", "2026-09-01", [
        {"airline": "Korean Air", "price": 481, "is_nonstop": 0, "duration_mins": 475},
        {"airline": "Korean Air", "price": 481, "is_nonstop": 0, "duration_mins": 475},
        {"airline": "Korean Air", "price": 481, "is_nonstop": 0, "duration_mins": 475},
    ]),
    ("ICN-HNL", "2026-11-25", [
        {"airline": "Perimeter Aviation", "price": 411, "is_nonstop": 1, "duration_mins": 500},
        {"airline": "Korean Air", "price": 481, "is_nonstop": 0, "duration_mins": 435},
        {"airline": "Korean Air", "price": 481, "is_nonstop": 0, "duration_mins": 435},
    ]),
    ("ICN-HNL", "2027-01-15", [
        {"airline": "Perimeter Aviation", "price": 513, "is_nonstop": 1, "duration_mins": 500},
        {"airline": "Korean Air", "price": 524, "is_nonstop": 0, "duration_mins": 435},
        {"airline": "Korean Air", "price": 524, "is_nonstop": 0, "duration_mins": 435},
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
