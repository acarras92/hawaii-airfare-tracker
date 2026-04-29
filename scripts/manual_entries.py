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
        {"airline": "Delta Air Lines", "price": 349, "is_nonstop": 1, "duration_mins": 460},
        {"airline": "Alaska Airlines", "price": 456, "is_nonstop": 1, "duration_mins": 475},
        {"airline": "Korean Air", "price": 513, "is_nonstop": 0, "duration_mins": 525},
    ]),
    ("HND-HNL", "2026-07-04", [
        {"airline": "Asiana Airlines", "price": 516, "is_nonstop": 0, "duration_mins": 555},
        {"airline": "Korean Air", "price": 522, "is_nonstop": 0, "duration_mins": 555},
        {"airline": "Asiana Airlines", "price": 526, "is_nonstop": 0, "duration_mins": 555},
    ]),
    # HND-HNL 2026-07-15: search returned no flights today; skipped
    ("HND-HNL", "2026-08-01", [
        {"airline": "Asiana Airlines", "price": 599, "is_nonstop": 0, "duration_mins": 555},
        {"airline": "Asiana Airlines", "price": 608, "is_nonstop": 0, "duration_mins": 555},
        {"airline": "Asiana Airlines", "price": 608, "is_nonstop": 0, "duration_mins": 555},
    ]),
    ("HND-HNL", "2026-09-01", [
        {"airline": "Delta Air Lines", "price": 349, "is_nonstop": 1, "duration_mins": 470},
        {"airline": "Korean Air", "price": 358, "is_nonstop": 0, "duration_mins": 530},
        {"airline": "Korean Air", "price": 367, "is_nonstop": 0, "duration_mins": 530},
    ]),
    ("HND-HNL", "2026-11-25", [
        {"airline": "Alaska Airlines", "price": 349, "is_nonstop": 1, "duration_mins": 435},
        {"airline": "Alaska Airlines", "price": 349, "is_nonstop": 1, "duration_mins": 435},
        {"airline": "Delta Air Lines", "price": 349, "is_nonstop": 1, "duration_mins": 445},
    ]),
    ("HND-HNL", "2026-12-20", [
        {"airline": "Delta Air Lines", "price": 350, "is_nonstop": 1, "duration_mins": 420},
        {"airline": "Japan Airlines", "price": 407, "is_nonstop": 0, "duration_mins": 455},
        {"airline": "Japan Airlines", "price": 407, "is_nonstop": 0, "duration_mins": 455},
    ]),
    ("HND-HNL", "2027-01-15", [
        {"airline": "Delta Air Lines", "price": 434, "is_nonstop": 1, "duration_mins": 410},
        {"airline": "Korean Air", "price": 513, "is_nonstop": 0, "duration_mins": 490},
        {"airline": "Asiana Airlines", "price": 516, "is_nonstop": 0, "duration_mins": 490},
    ]),

    # KIX-HNL
    ("KIX-HNL", "2026-06-15", [
        {"airline": "Japan Airlines", "price": 511, "is_nonstop": 0, "duration_mins": 475},
        {"airline": "Korean Air", "price": 511, "is_nonstop": 0, "duration_mins": 525},
        {"airline": "Korean Air", "price": 511, "is_nonstop": 0, "duration_mins": 525},
    ]),
    ("KIX-HNL", "2026-07-04", [
        {"airline": "Asiana Airlines", "price": 519, "is_nonstop": 0, "duration_mins": 555},
        {"airline": "Asiana Airlines", "price": 519, "is_nonstop": 0, "duration_mins": 555},
        {"airline": "Asiana Airlines", "price": 519, "is_nonstop": 0, "duration_mins": 555},
    ]),
    ("KIX-HNL", "2026-07-15", [
        {"airline": "Asiana Airlines", "price": 519, "is_nonstop": 0, "duration_mins": 555},
        {"airline": "Asiana Airlines", "price": 519, "is_nonstop": 0, "duration_mins": 555},
        {"airline": "Asiana Airlines", "price": 529, "is_nonstop": 0, "duration_mins": 555},
    ]),
    # KIX-HNL 2026-08-01: search returned no flights today; skipped
    ("KIX-HNL", "2026-09-01", [
        {"airline": "Korean Air", "price": 361, "is_nonstop": 0, "duration_mins": 530},
        {"airline": "Korean Air", "price": 361, "is_nonstop": 0, "duration_mins": 530},
        {"airline": "Korean Air", "price": 361, "is_nonstop": 0, "duration_mins": 530},
    ]),
    ("KIX-HNL", "2026-11-25", [
        {"airline": "Korean Air", "price": 361, "is_nonstop": 0, "duration_mins": 490},
        {"airline": "Korean Air", "price": 361, "is_nonstop": 0, "duration_mins": 490},
        {"airline": "Korean Air", "price": 370, "is_nonstop": 0, "duration_mins": 490},
    ]),
    ("KIX-HNL", "2026-12-20", [
        {"airline": "Japan Airlines", "price": 404, "is_nonstop": 0, "duration_mins": 435},
        {"airline": "Japan Airlines", "price": 404, "is_nonstop": 0, "duration_mins": 435},
        {"airline": "Japan Airlines", "price": 489, "is_nonstop": 0, "duration_mins": 435},
    ]),
    ("KIX-HNL", "2027-01-15", [
        {"airline": "Korean Air", "price": 516, "is_nonstop": 0, "duration_mins": 490},
        {"airline": "Korean Air", "price": 516, "is_nonstop": 0, "duration_mins": 490},
        {"airline": "Korean Air", "price": 516, "is_nonstop": 0, "duration_mins": 490},
    ]),

    # ICN-HNL (3 missing; earlier dates aggregated from tool-results files)
    ("ICN-HNL", "2026-07-04", [
        {"airline": "Korean Air", "price": 719, "is_nonstop": 0, "duration_mins": 475},
        {"airline": "Asiana Airlines", "price": 769, "is_nonstop": 1, "duration_mins": 555},
        {"airline": "Korean Air", "price": 881, "is_nonstop": 0, "duration_mins": 475},
    ]),
    ("ICN-HNL", "2026-12-20", [
        {"airline": "Korean Air", "price": 565, "is_nonstop": 0, "duration_mins": 455},
        {"airline": "Korean Air", "price": 577, "is_nonstop": 0, "duration_mins": 435},
        {"airline": "Korean Air", "price": 577, "is_nonstop": 0, "duration_mins": 435},
    ]),
    ("ICN-HNL", "2027-01-15", [
        {"airline": "Perimeter Aviation", "price": 558, "is_nonstop": 1, "duration_mins": 500},
        {"airline": "Korean Air", "price": 624, "is_nonstop": 0, "duration_mins": 435},
        {"airline": "Korean Air", "price": 624, "is_nonstop": 0, "duration_mins": 435},
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
