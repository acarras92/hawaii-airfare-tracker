#!/usr/bin/env python3
"""Merge manually-extracted top-3 fares for inline-response corridors into mcp_flights.json.

These corridors (HND, KIX, ICN origin) often return small inline responses
that do NOT get saved to the session's tool-results dir, so they need manual
population. Duration estimates are end-to-end trip time in minutes.
"""
import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "data" / "mcp_flights.json"


# Manual entries — top 3 cheapest non-ghost fares per (corridor, date), observed today.
MANUAL = [
    # HND-HNL
    ("HND-HNL", "2026-06-15", [
        {"airline": "Delta Air Lines", "price": 461, "is_nonstop": 1, "duration_mins": 460},
        {"airline": "Korean Air", "price": 598, "is_nonstop": 0, "duration_mins": 525},
        {"airline": "Korean Air", "price": 613, "is_nonstop": 0, "duration_mins": 510},
    ]),
    ("HND-HNL", "2026-07-04", [
        {"airline": "Delta Air Lines", "price": 461, "is_nonstop": 1, "duration_mins": 473},
        {"airline": "Korean Air", "price": 608, "is_nonstop": 0, "duration_mins": 555},
        {"airline": "Korean Air", "price": 617, "is_nonstop": 0, "duration_mins": 555},
    ]),
    ("HND-HNL", "2026-07-15", [
        {"airline": "Korean Air", "price": 470, "is_nonstop": 0, "duration_mins": 530},
        {"airline": "Korean Air", "price": 479, "is_nonstop": 0, "duration_mins": 530},
        {"airline": "Korean Air", "price": 479, "is_nonstop": 0, "duration_mins": 530},
    ]),
    ("HND-HNL", "2026-08-01", [
        {"airline": "Asiana Airlines", "price": 715, "is_nonstop": 0, "duration_mins": 555},
        {"airline": "Asiana Airlines", "price": 725, "is_nonstop": 0, "duration_mins": 555},
        {"airline": "Asiana Airlines", "price": 725, "is_nonstop": 0, "duration_mins": 555},
    ]),
    ("HND-HNL", "2026-09-01", [
        {"airline": "Delta Air Lines", "price": 461, "is_nonstop": 1, "duration_mins": 470},
        {"airline": "Korean Air", "price": 470, "is_nonstop": 0, "duration_mins": 530},
        {"airline": "Korean Air", "price": 479, "is_nonstop": 0, "duration_mins": 530},
    ]),
    ("HND-HNL", "2026-11-25", [
        {"airline": "Alaska Airlines", "price": 454, "is_nonstop": 1, "duration_mins": 435},
        {"airline": "Alaska Airlines", "price": 454, "is_nonstop": 1, "duration_mins": 435},
        {"airline": "Delta Air Lines", "price": 461, "is_nonstop": 1, "duration_mins": 445},
    ]),
    ("HND-HNL", "2026-12-20", [
        {"airline": "Delta Air Lines", "price": 461, "is_nonstop": 1, "duration_mins": 420},
        {"airline": "Japan Airlines", "price": 515, "is_nonstop": 0, "duration_mins": 455},
        {"airline": "Japan Airlines", "price": 515, "is_nonstop": 0, "duration_mins": 455},
    ]),
    ("HND-HNL", "2027-01-15", [
        {"airline": "Delta Air Lines", "price": 461, "is_nonstop": 1, "duration_mins": 410},
        {"airline": "Korean Air", "price": 584, "is_nonstop": 0, "duration_mins": 490},
        {"airline": "Korean Air", "price": 598, "is_nonstop": 0, "duration_mins": 490},
    ]),

    # KIX-HNL
    ("KIX-HNL", "2026-06-15", [
        {"airline": "Korean Air", "price": 472, "is_nonstop": 0, "duration_mins": 510},
        {"airline": "Korean Air", "price": 472, "is_nonstop": 0, "duration_mins": 510},
        {"airline": "Korean Air", "price": 472, "is_nonstop": 0, "duration_mins": 510},
    ]),
    ("KIX-HNL", "2026-07-04", [
        {"airline": "Korean Air", "price": 473, "is_nonstop": 0, "duration_mins": 530},
        {"airline": "Korean Air", "price": 473, "is_nonstop": 0, "duration_mins": 530},
        {"airline": "Korean Air", "price": 473, "is_nonstop": 0, "duration_mins": 530},
    ]),
    ("KIX-HNL", "2026-07-15", [
        {"airline": "Korean Air", "price": 472, "is_nonstop": 0, "duration_mins": 530},
        {"airline": "Korean Air", "price": 472, "is_nonstop": 0, "duration_mins": 530},
        {"airline": "Korean Air", "price": 472, "is_nonstop": 0, "duration_mins": 530},
    ]),
    ("KIX-HNL", "2026-08-01", [
        {"airline": "Asiana Airlines", "price": 699, "is_nonstop": 0, "duration_mins": 555},
        {"airline": "Asiana Airlines", "price": 699, "is_nonstop": 0, "duration_mins": 555},
        {"airline": "Asiana Airlines", "price": 699, "is_nonstop": 0, "duration_mins": 555},
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
        {"airline": "Japan Airlines", "price": 517, "is_nonstop": 0, "duration_mins": 435},
        {"airline": "Japan Airlines", "price": 517, "is_nonstop": 0, "duration_mins": 435},
        {"airline": "Japan Airlines", "price": 597, "is_nonstop": 0, "duration_mins": 435},
    ]),
    ("KIX-HNL", "2027-01-15", [
        {"airline": "Korean Air", "price": 601, "is_nonstop": 0, "duration_mins": 490},
        {"airline": "Korean Air", "price": 601, "is_nonstop": 0, "duration_mins": 490},
        {"airline": "Korean Air", "price": 601, "is_nonstop": 0, "duration_mins": 490},
    ]),

    # ICN-HNL (only 07-04 missing today; other dates aggregated from tool-results files)
    ("ICN-HNL", "2026-07-04", [
        {"airline": "Korean Air", "price": 725, "is_nonstop": 0, "duration_mins": 475},
        {"airline": "Korean Air", "price": 725, "is_nonstop": 0, "duration_mins": 475},
        {"airline": "Korean Air", "price": 820, "is_nonstop": 0, "duration_mins": 475},
    ]),
]


def main():
    existing = json.loads(OUT.read_text(encoding="utf-8"))
    by_key = {(e["corridor"], e["target_date"]): e for e in existing}
    for corridor, target, fares in MANUAL:
        by_key[(corridor, target)] = {
            "corridor": corridor,
            "target_date": target,
            "fares": fares,
        }

    CORRIDORS = ["LAX-HNL", "SFO-HNL", "JFK-HNL", "SEA-HNL", "LAX-OGG", "SFO-OGG",
                 "NRT-HNL", "HND-HNL", "KIX-HNL", "ICN-HNL"]
    TARGETS = ["2026-06-15", "2026-07-04", "2026-07-15", "2026-08-01",
               "2026-09-01", "2026-11-25", "2026-12-20", "2027-01-15"]

    out = []
    missing = []
    for c in CORRIDORS:
        for t in TARGETS:
            k = (c, t)
            if k in by_key:
                out.append(by_key[k])
            else:
                missing.append(k)

    OUT.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"Wrote {len(out)}/80 entries. Missing: {missing}")


if __name__ == "__main__":
    main()
