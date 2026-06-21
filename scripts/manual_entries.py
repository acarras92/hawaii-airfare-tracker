#!/usr/bin/env python3
"""Merge manually-extracted top-3 fares for inline-response corridors into mcp_flights.json.

These corridors (HND, KIX, ICN origin, plus some NRT dates) often return small
inline responses that do NOT get saved to the session's tool-results dir, so they
need manual population. Duration values mirror the trans-Pacific leg duration the
aggregator would emit (last-leg duration for connections, single-leg for nonstops)
to stay consistent with the rest of the dataset.

Refreshed 2026-06-21. The flight-search MCP was heavily degraded this session and
returned empty (count 0) for many corridors. HND and KIX produced ZERO files in any
session, so every HND/KIX combo MUST be overlaid here or it is dropped entirely.
Today's fresh inline captures: HND 07-04/07-15/09-01/12-20/01-15, KIX
07-04/07-15/08-01/11-25/12-20, ICN 07-04/07-15/09-01, NRT 07-04/07-15. Four combos
came back empty on every retry and CARRY FORWARD the 2026-06-20 values (no fresh
data available): HND-HNL 08-01, HND-HNL 11-25, KIX-HNL 09-01, KIX-HNL 01-15.
NRT-HNL 11-25/12-20/01-15 saved to files this session and are NOT listed here (the
overlay would clobber fresh file data). ICN 08-01/11-25/12-20/01-15 and NRT
08-01/09-01 came up empty but are backfilled by the aggregator from prior-session
files, so they are left to the aggregator rather than overlaid with stale values.
2026-06-15 is in the past (today is 2026-06-21) and is omitted entirely.
"""
import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "data" / "mcp_flights.json"

# Manual entries -- top 3 cheapest non-ghost fares per (corridor, date), observed 2026-06-21.
MANUAL = [
    # NRT-HNL (only 07-04 / 07-15 came inline; other NRT dates are file-based this session)
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

    # HND-HNL (all 7 overlaid; 08-01 and 11-25 carry forward 2026-06-20 -- empty today)
    ("HND-HNL", "2026-07-04", [
        {"airline": "Alaska Airlines", "price": 603, "is_nonstop": 1, "duration_mins": 475},
        {"airline": "Alaska Airlines", "price": 603, "is_nonstop": 1, "duration_mins": 475},
        {"airline": "Korean Air", "price": 645, "is_nonstop": 0, "duration_mins": 530},
    ]),
    ("HND-HNL", "2026-07-15", [
        {"airline": "Alaska Airlines", "price": 553, "is_nonstop": 1, "duration_mins": 475},
        {"airline": "Alaska Airlines", "price": 553, "is_nonstop": 1, "duration_mins": 475},
        {"airline": "Korean Air", "price": 562, "is_nonstop": 0, "duration_mins": 530},
    ]),
    ("HND-HNL", "2026-08-01", [  # carry forward 2026-06-20 (empty today)
        {"airline": "Delta Air Lines", "price": 770, "is_nonstop": 1, "duration_mins": 474},
        {"airline": "Alaska Airlines", "price": 811, "is_nonstop": 1, "duration_mins": 475},
        {"airline": "Alaska Airlines", "price": 811, "is_nonstop": 1, "duration_mins": 475},
    ]),
    ("HND-HNL", "2026-09-01", [
        {"airline": "Alaska Airlines", "price": 346, "is_nonstop": 1, "duration_mins": 475},
        {"airline": "Delta Air Lines", "price": 448, "is_nonstop": 1, "duration_mins": 470},
        {"airline": "Korean Air", "price": 456, "is_nonstop": 0, "duration_mins": 530},
    ]),
    ("HND-HNL", "2026-11-25", [  # carry forward 2026-06-20 (empty today)
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
        {"airline": "Korean Air", "price": 581, "is_nonstop": 0, "duration_mins": 490},
        {"airline": "Korean Air", "price": 586, "is_nonstop": 0, "duration_mins": 490},
    ]),

    # KIX-HNL (all 7 overlaid; 09-01 and 01-15 carry forward 2026-06-20 -- empty today)
    ("KIX-HNL", "2026-07-04", [
        {"airline": "Japan Airlines", "price": 403, "is_nonstop": 0, "duration_mins": 475},
        {"airline": "Japan Airlines", "price": 403, "is_nonstop": 0, "duration_mins": 475},
        {"airline": "Korean Air", "price": 434, "is_nonstop": 0, "duration_mins": 530},
    ]),
    ("KIX-HNL", "2026-07-15", [
        {"airline": "Korean Air", "price": 434, "is_nonstop": 0, "duration_mins": 530},
        {"airline": "Korean Air", "price": 434, "is_nonstop": 0, "duration_mins": 530},
        {"airline": "Korean Air", "price": 434, "is_nonstop": 0, "duration_mins": 530},
    ]),
    ("KIX-HNL", "2026-08-01", [
        {"airline": "All Nippon Airways", "price": 829, "is_nonstop": 0, "duration_mins": 474},
        {"airline": "All Nippon Airways", "price": 829, "is_nonstop": 0, "duration_mins": 474},
        {"airline": "All Nippon Airways", "price": 829, "is_nonstop": 0, "duration_mins": 474},
    ]),
    ("KIX-HNL", "2026-09-01", [  # carry forward 2026-06-20 (empty today)
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
    ("KIX-HNL", "2027-01-15", [  # carry forward 2026-06-20 (empty today)
        {"airline": "Korean Air", "price": 584, "is_nonstop": 0, "duration_mins": 490},
        {"airline": "Korean Air", "price": 584, "is_nonstop": 0, "duration_mins": 490},
        {"airline": "Korean Air", "price": 584, "is_nonstop": 0, "duration_mins": 490},
    ]),

    # ICN-HNL (07-04 / 07-15 / 09-01 came inline; other ICN dates were empty and are
    # left to the aggregator's backfill from prior-session files)
    ("ICN-HNL", "2026-07-04", [
        {"airline": "Korean Air", "price": 534, "is_nonstop": 0, "duration_mins": 475},
        {"airline": "Korean Air", "price": 534, "is_nonstop": 0, "duration_mins": 475},
        {"airline": "Korean Air", "price": 594, "is_nonstop": 0, "duration_mins": 510},
    ]),
    ("ICN-HNL", "2026-07-15", [
        {"airline": "Korean Air", "price": 476, "is_nonstop": 0, "duration_mins": 510},
        {"airline": "Korean Air", "price": 476, "is_nonstop": 0, "duration_mins": 510},
        {"airline": "Perimeter Aviation", "price": 514, "is_nonstop": 1, "duration_mins": 530},
    ]),
    ("ICN-HNL", "2026-09-01", [
        {"airline": "Korean Air", "price": 482, "is_nonstop": 0, "duration_mins": 475},
        {"airline": "Korean Air", "price": 482, "is_nonstop": 0, "duration_mins": 475},
        {"airline": "Korean Air", "price": 482, "is_nonstop": 0, "duration_mins": 475},
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
