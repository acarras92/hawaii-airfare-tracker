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

# Manual entries — top 3 cheapest non-ghost fares per (corridor, date), observed 2026-06-18.
# Today: all HND, all KIX, and all ICN returned inline (not saved to files), plus NRT-HNL
# 2026-07-04 which also came inline. The aggregator silently BACKFILLS the inline NRT/ICN
# combos from stale prior-session files (they don't show as "missing"), so they MUST be
# overlaid here with today's fresh top-3. The other NRT dates saved to files and are picked
# up by the aggregator — do NOT add them here or this overlay would clobber fresh file data.
# 2026-06-15 is now in the past (today is 2026-06-18) and is omitted entirely.
MANUAL = [
    # NRT-HNL (only 07-04 came inline; other NRT dates are file-based)
    ("NRT-HNL", "2026-07-04", [
        {"airline": "Korean Air", "price": 611, "is_nonstop": 0, "duration_mins": 530},
        {"airline": "Japan Airlines", "price": 616, "is_nonstop": 0, "duration_mins": 510},
        {"airline": "Korean Air", "price": 642, "is_nonstop": 0, "duration_mins": 530},
    ]),

    # HND-HNL (all 7 returned inline)
    ("HND-HNL", "2026-07-04", [
        {"airline": "Alaska Airlines", "price": 605, "is_nonstop": 1, "duration_mins": 475},
        {"airline": "Alaska Airlines", "price": 605, "is_nonstop": 1, "duration_mins": 475},
        {"airline": "Korean Air", "price": 611, "is_nonstop": 0, "duration_mins": 530},
    ]),
    ("HND-HNL", "2026-07-15", [
        {"airline": "Alaska Airlines", "price": 511, "is_nonstop": 1, "duration_mins": 475},
        {"airline": "Alaska Airlines", "price": 511, "is_nonstop": 1, "duration_mins": 475},
        {"airline": "Korean Air", "price": 562, "is_nonstop": 0, "duration_mins": 530},
    ]),
    ("HND-HNL", "2026-08-01", [
        {"airline": "Korean Air", "price": 457, "is_nonstop": 0, "duration_mins": 530},
        {"airline": "Korean Air", "price": 467, "is_nonstop": 0, "duration_mins": 530},
        {"airline": "Korean Air", "price": 467, "is_nonstop": 0, "duration_mins": 530},
    ]),
    ("HND-HNL", "2026-09-01", [
        {"airline": "Delta Air Lines", "price": 448, "is_nonstop": 1, "duration_mins": 470},
        {"airline": "Alaska Airlines", "price": 449, "is_nonstop": 1, "duration_mins": 475},
        {"airline": "Korean Air", "price": 456, "is_nonstop": 0, "duration_mins": 530},
    ]),
    ("HND-HNL", "2026-11-25", [
        {"airline": "Delta Air Lines", "price": 448, "is_nonstop": 1, "duration_mins": 445},
        {"airline": "Alaska Airlines", "price": 449, "is_nonstop": 1, "duration_mins": 435},
        {"airline": "Alaska Airlines", "price": 449, "is_nonstop": 1, "duration_mins": 435},
    ]),
    ("HND-HNL", "2026-12-20", [
        {"airline": "Delta Air Lines", "price": 448, "is_nonstop": 1, "duration_mins": 420},
        {"airline": "Alaska Airlines", "price": 449, "is_nonstop": 1, "duration_mins": 435},
        {"airline": "Alaska Airlines", "price": 449, "is_nonstop": 1, "duration_mins": 435},
    ]),
    ("HND-HNL", "2027-01-15", [
        {"airline": "Delta Air Lines", "price": 448, "is_nonstop": 1, "duration_mins": 410},
        {"airline": "Korean Air", "price": 549, "is_nonstop": 0, "duration_mins": 460},
        {"airline": "Korean Air", "price": 567, "is_nonstop": 0, "duration_mins": 490},
    ]),

    # KIX-HNL (all 7 returned inline)
    ("KIX-HNL", "2026-07-04", [
        {"airline": "Korean Air", "price": 614, "is_nonstop": 0, "duration_mins": 530},
        {"airline": "Korean Air", "price": 614, "is_nonstop": 0, "duration_mins": 530},
        {"airline": "Korean Air", "price": 614, "is_nonstop": 0, "duration_mins": 530},
    ]),
    ("KIX-HNL", "2026-07-15", [
        {"airline": "Korean Air", "price": 564, "is_nonstop": 0, "duration_mins": 530},
        {"airline": "Korean Air", "price": 564, "is_nonstop": 0, "duration_mins": 530},
        {"airline": "Korean Air", "price": 564, "is_nonstop": 0, "duration_mins": 530},
    ]),
    ("KIX-HNL", "2026-08-01", [
        {"airline": "Korean Air", "price": 460, "is_nonstop": 0, "duration_mins": 530},
        {"airline": "Korean Air", "price": 460, "is_nonstop": 0, "duration_mins": 530},
        {"airline": "Korean Air", "price": 460, "is_nonstop": 0, "duration_mins": 530},
    ]),
    ("KIX-HNL", "2026-09-01", [
        {"airline": "Korean Air", "price": 459, "is_nonstop": 0, "duration_mins": 530},
        {"airline": "Korean Air", "price": 459, "is_nonstop": 0, "duration_mins": 530},
        {"airline": "Korean Air", "price": 459, "is_nonstop": 0, "duration_mins": 530},
    ]),
    ("KIX-HNL", "2026-11-25", [
        {"airline": "Korean Air", "price": 459, "is_nonstop": 0, "duration_mins": 490},
        {"airline": "Korean Air", "price": 459, "is_nonstop": 0, "duration_mins": 490},
        {"airline": "Korean Air", "price": 459, "is_nonstop": 0, "duration_mins": 490},
    ]),
    ("KIX-HNL", "2026-12-20", [
        {"airline": "Japan Airlines", "price": 502, "is_nonstop": 0, "duration_mins": 435},
        {"airline": "Japan Airlines", "price": 502, "is_nonstop": 0, "duration_mins": 435},
        {"airline": "Japan Airlines", "price": 506, "is_nonstop": 0, "duration_mins": 435},
    ]),
    ("KIX-HNL", "2027-01-15", [
        {"airline": "Korean Air", "price": 584, "is_nonstop": 0, "duration_mins": 490},
        {"airline": "Korean Air", "price": 584, "is_nonstop": 0, "duration_mins": 490},
        {"airline": "Korean Air", "price": 584, "is_nonstop": 0, "duration_mins": 490},
    ]),

    # ICN-HNL (all 7 returned inline)
    ("ICN-HNL", "2026-07-04", [
        {"airline": "Korean Air", "price": 530, "is_nonstop": 0, "duration_mins": 475},
        {"airline": "Korean Air", "price": 530, "is_nonstop": 0, "duration_mins": 475},
        {"airline": "Korean Air", "price": 530, "is_nonstop": 0, "duration_mins": 475},
    ]),
    ("ICN-HNL", "2026-07-15", [
        {"airline": "Perimeter Aviation", "price": 468, "is_nonstop": 1, "duration_mins": 530},
        {"airline": "Korean Air", "price": 488, "is_nonstop": 0, "duration_mins": 510},
        {"airline": "Asiana Airlines", "price": 521, "is_nonstop": 0, "duration_mins": 475},
    ]),
    ("ICN-HNL", "2026-08-01", [
        {"airline": "Korean Air", "price": 680, "is_nonstop": 0, "duration_mins": 510},
        {"airline": "Korean Air", "price": 692, "is_nonstop": 0, "duration_mins": 475},
        {"airline": "Korean Air", "price": 692, "is_nonstop": 0, "duration_mins": 475},
    ]),
    ("ICN-HNL", "2026-09-01", [
        {"airline": "Korean Air", "price": 466, "is_nonstop": 0, "duration_mins": 500},
        {"airline": "Korean Air", "price": 466, "is_nonstop": 0, "duration_mins": 500},
        {"airline": "Korean Air", "price": 478, "is_nonstop": 0, "duration_mins": 475},
    ]),
    ("ICN-HNL", "2026-11-25", [
        {"airline": "Perimeter Aviation", "price": 409, "is_nonstop": 1, "duration_mins": 500},
        {"airline": "Korean Air", "price": 478, "is_nonstop": 0, "duration_mins": 435},
        {"airline": "Korean Air", "price": 478, "is_nonstop": 0, "duration_mins": 435},
    ]),
    ("ICN-HNL", "2026-12-20", [
        {"airline": "Korean Air", "price": 543, "is_nonstop": 0, "duration_mins": 455},
        {"airline": "Korean Air", "price": 555, "is_nonstop": 0, "duration_mins": 435},
        {"airline": "Korean Air", "price": 555, "is_nonstop": 0, "duration_mins": 435},
    ]),
    ("ICN-HNL", "2027-01-15", [
        {"airline": "Perimeter Aviation", "price": 510, "is_nonstop": 1, "duration_mins": 500},
        {"airline": "Korean Air", "price": 521, "is_nonstop": 0, "duration_mins": 435},
        {"airline": "Korean Air", "price": 521, "is_nonstop": 0, "duration_mins": 435},
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
