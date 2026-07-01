#!/usr/bin/env python3
"""Merge manually-extracted top-3 fares for inline-response corridors into mcp_flights.json.

These corridors (HND, KIX, ICN origin, plus some NRT dates) often return small
inline responses that do NOT get saved to the session's tool-results dir, so they
need manual population. Duration values mirror the trans-Pacific leg duration the
aggregator would emit (last-leg duration for connections, single-leg for nonstops)
to stay consistent with the rest of the dataset.

Refreshed 2026-07-01. The flight-search MCP was UP this session and returned full
fares for every corridor. HND and KIX produced ZERO files in any session (always
inline), so every live HND/KIX combo MUST be overlaid here or it is dropped.
NRT 07-04/07-15/08-01 and ICN 07-15/08-01/09-01/11-25/01-15 came inline today and
are overlaid with fresh values (the aggregator otherwise backfills them from stale
prior-session files -- confirmed today: it emitted NRT 07-04 $614/ICN 09-01 $483
from old sessions vs today's $462/$379). NRT 09-01/11-25/12-20/01-15 and
ICN 07-04/12-20 saved to files this session and are NOT listed here (the overlay
would clobber fresh file data). Several combos were transiently empty and returned
fares on retry: JFK 01-15, SEA 07-15/09-01, SFO-OGG 12-20 (all resolved to files);
HND 07-04/07-15 empty twice then filled on the 3rd attempt (overlaid here).
2026-06-15 is in the past (today is 2026-07-01) and is omitted entirely.
"""
import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "data" / "mcp_flights.json"

# Manual entries -- top 3 cheapest non-ghost fares per (corridor, date), observed 2026-07-01.
MANUAL = [
    # NRT-HNL (07-04 / 07-15 / 08-01 came inline; 09-01 / 11-25 / 12-20 / 01-15 are file-based this session)
    ("NRT-HNL", "2026-07-04", [
        {"airline": "Korean Air", "price": 462, "is_nonstop": 0, "duration_mins": 530},
        {"airline": "Korean Air", "price": 462, "is_nonstop": 0, "duration_mins": 530},
        {"airline": "Korean Air", "price": 462, "is_nonstop": 0, "duration_mins": 530},
    ]),
    ("NRT-HNL", "2026-07-15", [
        {"airline": "Korean Air", "price": 462, "is_nonstop": 0, "duration_mins": 530},
        {"airline": "Korean Air", "price": 462, "is_nonstop": 0, "duration_mins": 530},
        {"airline": "Korean Air", "price": 462, "is_nonstop": 0, "duration_mins": 530},
    ]),
    ("NRT-HNL", "2026-08-01", [
        {"airline": "Korean Air", "price": 616, "is_nonstop": 0, "duration_mins": 530},
        {"airline": "Zipair", "price": 720, "is_nonstop": 1, "duration_mins": 460},
        {"airline": "Korean Air", "price": 782, "is_nonstop": 0, "duration_mins": 530},
    ]),

    # HND-HNL (all 7 live dates overlaid -- entirely missing from aggregator)
    ("HND-HNL", "2026-07-04", [
        {"airline": "Alaska Airlines", "price": 379, "is_nonstop": 1, "duration_mins": 475},
        {"airline": "Alaska Airlines", "price": 379, "is_nonstop": 1, "duration_mins": 475},
        {"airline": "Japan Airlines", "price": 436, "is_nonstop": 0, "duration_mins": 510},
    ]),
    ("HND-HNL", "2026-07-15", [
        {"airline": "Alaska Airlines", "price": 597, "is_nonstop": 1, "duration_mins": 475},
        {"airline": "Alaska Airlines", "price": 597, "is_nonstop": 1, "duration_mins": 475},
        {"airline": "Japan Airlines", "price": 653, "is_nonstop": 0, "duration_mins": 510},
    ]),
    ("HND-HNL", "2026-08-01", [
        {"airline": "Alaska Airlines", "price": 854, "is_nonstop": 1, "duration_mins": 475},
        {"airline": "Alaska Airlines", "price": 854, "is_nonstop": 1, "duration_mins": 475},
        {"airline": "Japan Airlines", "price": 887, "is_nonstop": 0, "duration_mins": 480},
    ]),
    ("HND-HNL", "2026-09-01", [
        {"airline": "Philippine Airlines", "price": 449, "is_nonstop": 0, "duration_mins": 635},
        {"airline": "Delta Air Lines", "price": 479, "is_nonstop": 1, "duration_mins": 470},
        {"airline": "Korean Air", "price": 487, "is_nonstop": 0, "duration_mins": 530},
    ]),
    ("HND-HNL", "2026-11-25", [
        {"airline": "Delta Air Lines", "price": 479, "is_nonstop": 1, "duration_mins": 445},
        {"airline": "Korean Air", "price": 487, "is_nonstop": 0, "duration_mins": 490},
        {"airline": "Alaska Airlines", "price": 492, "is_nonstop": 1, "duration_mins": 435},
    ]),
    ("HND-HNL", "2026-12-20", [
        {"airline": "Delta Air Lines", "price": 480, "is_nonstop": 1, "duration_mins": 420},
        {"airline": "Alaska Airlines", "price": 492, "is_nonstop": 1, "duration_mins": 435},
        {"airline": "Alaska Airlines", "price": 492, "is_nonstop": 1, "duration_mins": 435},
    ]),
    ("HND-HNL", "2027-01-15", [
        {"airline": "Delta Air Lines", "price": 479, "is_nonstop": 1, "duration_mins": 410},
        {"airline": "Korean Air", "price": 605, "is_nonstop": 0, "duration_mins": 490},
        {"airline": "Korean Air", "price": 610, "is_nonstop": 0, "duration_mins": 490},
    ]),

    # KIX-HNL (all 7 live dates overlaid -- entirely missing from aggregator)
    ("KIX-HNL", "2026-07-04", [
        {"airline": "Japan Airlines", "price": 433, "is_nonstop": 0, "duration_mins": 475},
        {"airline": "Japan Airlines", "price": 433, "is_nonstop": 0, "duration_mins": 475},
        {"airline": "Korean Air", "price": 465, "is_nonstop": 0, "duration_mins": 530},
    ]),
    ("KIX-HNL", "2026-07-15", [
        {"airline": "Korean Air", "price": 465, "is_nonstop": 0, "duration_mins": 530},
        {"airline": "Korean Air", "price": 465, "is_nonstop": 0, "duration_mins": 530},
        {"airline": "Korean Air", "price": 465, "is_nonstop": 0, "duration_mins": 530},
    ]),
    ("KIX-HNL", "2026-08-01", [
        {"airline": "Alaska Airlines", "price": 837, "is_nonstop": 1, "duration_mins": 510},
        {"airline": "Japan Airlines", "price": 873, "is_nonstop": 0, "duration_mins": 475},
        {"airline": "Japan Airlines", "price": 873, "is_nonstop": 0, "duration_mins": 475},
    ]),
    ("KIX-HNL", "2026-09-01", [
        {"airline": "Korean Air", "price": 490, "is_nonstop": 0, "duration_mins": 530},
        {"airline": "Korean Air", "price": 490, "is_nonstop": 0, "duration_mins": 530},
        {"airline": "Korean Air", "price": 490, "is_nonstop": 0, "duration_mins": 530},
    ]),
    ("KIX-HNL", "2026-11-25", [
        {"airline": "Korean Air", "price": 490, "is_nonstop": 0, "duration_mins": 490},
        {"airline": "Korean Air", "price": 490, "is_nonstop": 0, "duration_mins": 490},
        {"airline": "Korean Air", "price": 490, "is_nonstop": 0, "duration_mins": 490},
    ]),
    ("KIX-HNL", "2026-12-20", [
        {"airline": "Japan Airlines", "price": 546, "is_nonstop": 0, "duration_mins": 435},
        {"airline": "Japan Airlines", "price": 546, "is_nonstop": 0, "duration_mins": 435},
        {"airline": "Japan Airlines", "price": 546, "is_nonstop": 0, "duration_mins": 435},
    ]),
    ("KIX-HNL", "2027-01-15", [
        {"airline": "Korean Air", "price": 490, "is_nonstop": 0, "duration_mins": 460},
        {"airline": "Korean Air", "price": 490, "is_nonstop": 0, "duration_mins": 460},
        {"airline": "Korean Air", "price": 594, "is_nonstop": 0, "duration_mins": 490},
    ]),

    # ICN-HNL (07-15 / 08-01 / 09-01 / 11-25 / 01-15 came inline; 07-04 / 12-20 are file-based this session)
    ("ICN-HNL", "2026-07-15", [
        {"airline": "Perimeter Aviation", "price": 410, "is_nonstop": 1, "duration_mins": 530},
        {"airline": "Korean Air", "price": 472, "is_nonstop": 0, "duration_mins": 510},
        {"airline": "Asiana Airlines", "price": 484, "is_nonstop": 0, "duration_mins": 475},
    ]),
    ("ICN-HNL", "2026-08-01", [
        {"airline": "Korean Air", "price": 677, "is_nonstop": 0, "duration_mins": 510},
        {"airline": "Alaska Airlines", "price": 810, "is_nonstop": 0, "duration_mins": 356},
        {"airline": "Alaska Airlines", "price": 810, "is_nonstop": 0, "duration_mins": 369},
    ]),
    ("ICN-HNL", "2026-09-01", [
        {"airline": "Asiana Airlines", "price": 379, "is_nonstop": 0, "duration_mins": 500},
        {"airline": "Korean Air", "price": 407, "is_nonstop": 0, "duration_mins": 500},
        {"airline": "Korean Air", "price": 424, "is_nonstop": 0, "duration_mins": 500},
    ]),
    ("ICN-HNL", "2026-11-25", [
        {"airline": "Perimeter Aviation", "price": 435, "is_nonstop": 1, "duration_mins": 500},
        {"airline": "Korean Air", "price": 465, "is_nonstop": 0, "duration_mins": 455},
        {"airline": "Philippine Airlines", "price": 474, "is_nonstop": 0, "duration_mins": 620},
    ]),
    ("ICN-HNL", "2027-01-15", [
        {"airline": "Perimeter Aviation", "price": 451, "is_nonstop": 1, "duration_mins": 500},
        {"airline": "Korean Air", "price": 520, "is_nonstop": 0, "duration_mins": 435},
        {"airline": "Korean Air", "price": 533, "is_nonstop": 0, "duration_mins": 455},
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
