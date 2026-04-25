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
        {"airline": "Delta Air Lines", "price": 352, "is_nonstop": 1, "duration_mins": 460},
        {"airline": "Korean Air", "price": 516, "is_nonstop": 0, "duration_mins": 680},
        {"airline": "Asiana Airlines", "price": 520, "is_nonstop": 0, "duration_mins": 685},
    ]),
    ("HND-HNL", "2026-07-04", [
        {"airline": "Asiana Airlines", "price": 520, "is_nonstop": 0, "duration_mins": 715},
        {"airline": "Korean Air", "price": 526, "is_nonstop": 0, "duration_mins": 700},
        {"airline": "Asiana Airlines", "price": 529, "is_nonstop": 0, "duration_mins": 695},
    ]),
    ("HND-HNL", "2026-07-15", [
        {"airline": "Asiana Airlines", "price": 520, "is_nonstop": 0, "duration_mins": 715},
        {"airline": "Korean Air", "price": 526, "is_nonstop": 0, "duration_mins": 700},
        {"airline": "Korean Air", "price": 526, "is_nonstop": 0, "duration_mins": 695},
    ]),
    ("HND-HNL", "2026-08-01", [
        {"airline": "Delta Air Lines", "price": 519, "is_nonstop": 1, "duration_mins": 474},
        {"airline": "Asiana Airlines", "price": 603, "is_nonstop": 0, "duration_mins": 715},
        {"airline": "Asiana Airlines", "price": 613, "is_nonstop": 0, "duration_mins": 695},
    ]),
    ("HND-HNL", "2026-09-01", [
        {"airline": "Delta Air Lines", "price": 352, "is_nonstop": 1, "duration_mins": 470},
        {"airline": "Korean Air", "price": 360, "is_nonstop": 0, "duration_mins": 685},
        {"airline": "Korean Air", "price": 370, "is_nonstop": 0, "duration_mins": 675},
    ]),
    ("HND-HNL", "2026-11-25", [
        {"airline": "Alaska Airlines", "price": 348, "is_nonstop": 1, "duration_mins": 435},
        {"airline": "Alaska Airlines", "price": 348, "is_nonstop": 1, "duration_mins": 435},
        {"airline": "Delta Air Lines", "price": 352, "is_nonstop": 1, "duration_mins": 445},
    ]),
    ("HND-HNL", "2026-12-20", [
        {"airline": "Alaska Airlines", "price": 348, "is_nonstop": 1, "duration_mins": 435},
        {"airline": "Alaska Airlines", "price": 348, "is_nonstop": 1, "duration_mins": 435},
        {"airline": "Delta Air Lines", "price": 352, "is_nonstop": 1, "duration_mins": 420},
    ]),
    ("HND-HNL", "2027-01-15", [
        {"airline": "Delta Air Lines", "price": 437, "is_nonstop": 1, "duration_mins": 410},
        {"airline": "Korean Air", "price": 502, "is_nonstop": 0, "duration_mins": 650},
        {"airline": "Korean Air", "price": 516, "is_nonstop": 0, "duration_mins": 660},
    ]),

    # KIX-HNL
    ("KIX-HNL", "2026-06-15", [
        {"airline": "Korean Air", "price": 519, "is_nonstop": 0, "duration_mins": 635},
        {"airline": "Asiana Airlines", "price": 523, "is_nonstop": 0, "duration_mins": 645},
        {"airline": "Asiana Airlines", "price": 523, "is_nonstop": 0, "duration_mins": 650},
    ]),
    ("KIX-HNL", "2026-07-04", [
        {"airline": "Korean Air", "price": 519, "is_nonstop": 0, "duration_mins": 665},
        {"airline": "Korean Air", "price": 519, "is_nonstop": 0, "duration_mins": 665},
        {"airline": "Korean Air", "price": 519, "is_nonstop": 0, "duration_mins": 665},
    ]),
    ("KIX-HNL", "2026-07-15", [
        {"airline": "Korean Air", "price": 519, "is_nonstop": 0, "duration_mins": 665},
        {"airline": "Korean Air", "price": 519, "is_nonstop": 0, "duration_mins": 665},
        {"airline": "Asiana Airlines", "price": 523, "is_nonstop": 0, "duration_mins": 680},
    ]),
    ("KIX-HNL", "2026-08-01", [
        {"airline": "Asiana Airlines", "price": 587, "is_nonstop": 0, "duration_mins": 680},
        {"airline": "Asiana Airlines", "price": 587, "is_nonstop": 0, "duration_mins": 685},
        {"airline": "Asiana Airlines", "price": 587, "is_nonstop": 0, "duration_mins": 670},
    ]),
    ("KIX-HNL", "2026-09-01", [
        {"airline": "Korean Air", "price": 363, "is_nonstop": 0, "duration_mins": 640},
        {"airline": "Korean Air", "price": 363, "is_nonstop": 0, "duration_mins": 640},
        {"airline": "Korean Air", "price": 363, "is_nonstop": 0, "duration_mins": 640},
    ]),
    ("KIX-HNL", "2026-11-25", [
        {"airline": "Korean Air", "price": 363, "is_nonstop": 0, "duration_mins": 600},
        {"airline": "Korean Air", "price": 363, "is_nonstop": 0, "duration_mins": 620},
        {"airline": "Korean Air", "price": 373, "is_nonstop": 0, "duration_mins": 615},
    ]),
    ("KIX-HNL", "2026-12-20", [
        {"airline": "Japan Airlines", "price": 405, "is_nonstop": 0, "duration_mins": 500},
        {"airline": "Japan Airlines", "price": 405, "is_nonstop": 0, "duration_mins": 500},
        {"airline": "Alaska Airlines", "price": 506, "is_nonstop": 1, "duration_mins": 455},
    ]),
    ("KIX-HNL", "2027-01-15", [
        {"airline": "Korean Air", "price": 519, "is_nonstop": 0, "duration_mins": 600},
        {"airline": "Korean Air", "price": 519, "is_nonstop": 0, "duration_mins": 615},
        {"airline": "Korean Air", "price": 519, "is_nonstop": 0, "duration_mins": 620},
    ]),

    # ICN-HNL (only 3 missing; earlier dates aggregated from tool-results files)
    ("ICN-HNL", "2026-07-04", [
        {"airline": "Asiana Airlines", "price": 770, "is_nonstop": 1, "duration_mins": 555},
        {"airline": "Alaska Airlines", "price": 877, "is_nonstop": 0, "duration_mins": 986},
        {"airline": "Alaska Airlines", "price": 877, "is_nonstop": 0, "duration_mins": 999},
    ]),
    ("ICN-HNL", "2026-12-20", [
        {"airline": "Perimeter Aviation", "price": 594, "is_nonstop": 1, "duration_mins": 500},
        {"airline": "Korean Air", "price": 646, "is_nonstop": 0, "duration_mins": 570},
        {"airline": "Korean Air", "price": 659, "is_nonstop": 0, "duration_mins": 585},
    ]),
    ("ICN-HNL", "2027-01-15", [
        {"airline": "Perimeter Aviation", "price": 559, "is_nonstop": 1, "duration_mins": 500},
        {"airline": "Korean Air", "price": 706, "is_nonstop": 0, "duration_mins": 585},
        {"airline": "Korean Air", "price": 706, "is_nonstop": 0, "duration_mins": 585},
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
