#!/usr/bin/env python3
"""Merge manually-extracted top-3 fares for HND, KIX, ICN corridors into mcp_flights.json."""
import json
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "data" / "mcp_flights.json"


def dur(dep, arr):
    """Compute minutes between ISO timestamps."""
    return int((datetime.fromisoformat(arr) - datetime.fromisoformat(dep)).total_seconds() // 60)


# Manual entries extracted from inline MCP responses (post-retry with checked_bags=1)
# These prices are slightly higher than no-bag baseline due to bag fee inclusion.
MANUAL = [
    # HND-HNL
    ("HND-HNL", "2026-06-15", [
        {"airline": "Delta Air Lines", "price": 350, "is_nonstop": 1, "duration_mins": 460},
        {"airline": "Korean Air", "price": 514, "is_nonstop": 0, "duration_mins": dur("2026-06-15T02:00:00", "2026-06-15T10:10:00")},
        {"airline": "Asiana Airlines", "price": 518, "is_nonstop": 0, "duration_mins": dur("2026-06-15T01:30:00", "2026-06-15T10:10:00")},
    ]),
    ("HND-HNL", "2026-07-04", [
        {"airline": "Korean Air", "price": 495, "is_nonstop": 0, "duration_mins": dur("2026-07-04T09:20:00", "2026-07-04T10:40:00")+24*60},
        {"airline": "Asiana Airlines", "price": 518, "is_nonstop": 0, "duration_mins": dur("2026-07-04T01:30:00", "2026-07-04T10:40:00")},
        {"airline": "Korean Air", "price": 519, "is_nonstop": 0, "duration_mins": dur("2026-07-04T12:35:00", "2026-07-04T10:40:00")+24*60},
    ]),
    ("HND-HNL", "2026-07-15", [
        {"airline": "Korean Air", "price": 495, "is_nonstop": 0, "duration_mins": dur("2026-07-15T09:20:00", "2026-07-15T10:40:00")+24*60},
        {"airline": "Korean Air", "price": 495, "is_nonstop": 0, "duration_mins": dur("2026-07-15T12:35:00", "2026-07-15T10:40:00")+24*60},
        {"airline": "Korean Air", "price": 506, "is_nonstop": 0, "duration_mins": dur("2026-07-15T09:20:00", "2026-07-15T10:55:00")+24*60},
    ]),
    ("HND-HNL", "2026-08-01", [
        {"airline": "Asiana Airlines", "price": 601, "is_nonstop": 0, "duration_mins": dur("2026-08-01T01:30:00", "2026-08-01T10:40:00")},
        {"airline": "Asiana Airlines", "price": 610, "is_nonstop": 0, "duration_mins": dur("2026-08-01T09:00:00", "2026-08-01T10:40:00")+24*60},
        {"airline": "Asiana Airlines", "price": 610, "is_nonstop": 0, "duration_mins": dur("2026-08-01T12:05:00", "2026-08-01T10:40:00")+24*60},
    ]),
    ("HND-HNL", "2026-09-01", [
        {"airline": "Delta Air Lines", "price": 350, "is_nonstop": 1, "duration_mins": 470},
        {"airline": "Korean Air", "price": 359, "is_nonstop": 0, "duration_mins": dur("2026-09-01T02:00:00", "2026-09-01T10:55:00")},
        {"airline": "Korean Air", "price": 369, "is_nonstop": 0, "duration_mins": dur("2026-09-01T09:20:00", "2026-09-01T10:55:00")+24*60},
    ]),
    ("HND-HNL", "2026-11-25", [
        {"airline": "Delta Air Lines", "price": 350, "is_nonstop": 1, "duration_mins": 445},
        {"airline": "Korean Air", "price": 365, "is_nonstop": 0, "duration_mins": dur("2026-11-25T09:45:00", "2026-11-25T09:45:00")+24*60},
        {"airline": "Korean Air", "price": 365, "is_nonstop": 0, "duration_mins": dur("2026-11-25T12:25:00", "2026-11-25T09:45:00")+24*60},
    ]),
    ("HND-HNL", "2026-12-20", [
        {"airline": "Delta Air Lines", "price": 351, "is_nonstop": 1, "duration_mins": 420},
        {"airline": "Alaska Airlines", "price": 526, "is_nonstop": 1, "duration_mins": 435},
        {"airline": "Alaska Airlines", "price": 526, "is_nonstop": 1, "duration_mins": 435},
    ]),
    ("HND-HNL", "2027-01-15", [
        {"airline": "Delta Air Lines", "price": 350, "is_nonstop": 1, "duration_mins": 410},
        {"airline": "Korean Air", "price": 495, "is_nonstop": 0, "duration_mins": dur("2027-01-15T09:45:00", "2027-01-15T09:30:00")+24*60},
        {"airline": "Korean Air", "price": 506, "is_nonstop": 0, "duration_mins": dur("2027-01-15T09:45:00", "2027-01-15T09:15:00")+24*60},
    ]),

    # KIX-HNL
    ("KIX-HNL", "2026-06-15", [
        {"airline": "Korean Air", "price": 497, "is_nonstop": 0, "duration_mins": dur("2026-06-15T12:25:00", "2026-06-15T10:10:00")+24*60},
        {"airline": "Korean Air", "price": 517, "is_nonstop": 0, "duration_mins": dur("2026-06-15T02:15:00", "2026-06-15T10:10:00")},
        {"airline": "Asiana Airlines", "price": 521, "is_nonstop": 0, "duration_mins": dur("2026-06-15T00:15:00", "2026-06-15T10:10:00")},
    ]),
    ("KIX-HNL", "2026-07-04", [
        {"airline": "Korean Air", "price": 497, "is_nonstop": 0, "duration_mins": dur("2026-07-04T12:25:00", "2026-07-04T10:40:00")+24*60},
        {"airline": "Asiana Airlines", "price": 521, "is_nonstop": 0, "duration_mins": dur("2026-07-04T09:30:00", "2026-07-04T10:40:00")+24*60},
        {"airline": "Asiana Airlines", "price": 521, "is_nonstop": 0, "duration_mins": dur("2026-07-04T10:30:00", "2026-07-04T10:40:00")+24*60},
    ]),
    ("KIX-HNL", "2026-07-15", [
        {"airline": "Korean Air", "price": 488, "is_nonstop": 0, "duration_mins": dur("2026-07-15T12:35:00", "2026-07-15T10:40:00")+24*60},
        {"airline": "Korean Air", "price": 503, "is_nonstop": 0, "duration_mins": dur("2026-07-15T12:25:00", "2026-07-15T10:40:00")+24*60},
        {"airline": "Korean Air", "price": 517, "is_nonstop": 0, "duration_mins": dur("2026-07-15T02:15:00", "2026-07-15T10:40:00")},
    ]),
    ("KIX-HNL", "2026-08-01", [
        {"airline": "Asiana Airlines", "price": 585, "is_nonstop": 0, "duration_mins": dur("2026-08-01T09:30:00", "2026-08-01T10:40:00")+24*60},
        {"airline": "Asiana Airlines", "price": 585, "is_nonstop": 0, "duration_mins": dur("2026-08-01T10:30:00", "2026-08-01T10:40:00")+24*60},
        {"airline": "Asiana Airlines", "price": 585, "is_nonstop": 0, "duration_mins": dur("2026-08-01T19:45:00", "2026-08-01T10:40:00")+2*24*60},
    ]),
    ("KIX-HNL", "2026-09-01", [
        {"airline": "Korean Air", "price": 362, "is_nonstop": 0, "duration_mins": dur("2026-09-01T02:15:00", "2026-09-01T10:55:00")},
        {"airline": "Korean Air", "price": 362, "is_nonstop": 0, "duration_mins": dur("2026-09-01T09:05:00", "2026-09-01T10:55:00")+24*60},
        {"airline": "Korean Air", "price": 362, "is_nonstop": 0, "duration_mins": dur("2026-09-01T12:35:00", "2026-09-01T10:55:00")+24*60},
    ]),
    ("KIX-HNL", "2026-11-25", [
        {"airline": "Korean Air", "price": 362, "is_nonstop": 0, "duration_mins": dur("2026-11-25T02:15:00", "2026-11-25T09:45:00")},
        {"airline": "Korean Air", "price": 447, "is_nonstop": 0, "duration_mins": dur("2026-11-25T11:55:00", "2026-11-25T09:45:00")+24*60},
        {"airline": "Korean Air", "price": 456, "is_nonstop": 0, "duration_mins": dur("2026-11-25T11:55:00", "2026-11-25T09:45:00")+24*60},
    ]),
    ("KIX-HNL", "2026-12-20", [
        {"airline": "Alaska Airlines", "price": 508, "is_nonstop": 1, "duration_mins": 455},
        {"airline": "Korean Air", "price": 525, "is_nonstop": 0, "duration_mins": dur("2026-12-20T09:00:00", "2026-12-20T09:30:00")+24*60},
        {"airline": "Korean Air", "price": 525, "is_nonstop": 0, "duration_mins": dur("2026-12-20T11:55:00", "2026-12-20T09:30:00")+24*60},
    ]),
    ("KIX-HNL", "2027-01-15", [
        {"airline": "Korean Air", "price": 488, "is_nonstop": 0, "duration_mins": dur("2027-01-15T09:00:00", "2027-01-15T09:30:00")+24*60},
        {"airline": "Korean Air", "price": 488, "is_nonstop": 0, "duration_mins": dur("2027-01-15T11:55:00", "2027-01-15T09:30:00")+24*60},
        {"airline": "Korean Air", "price": 503, "is_nonstop": 0, "duration_mins": dur("2027-01-15T11:55:00", "2027-01-15T09:30:00")+24*60},
    ]),

    # ICN-HNL (only 3 missing — others already aggregated from earlier saved files)
    ("ICN-HNL", "2026-07-04", [
        {"airline": "Asiana Airlines", "price": 769, "is_nonstop": 1, "duration_mins": 555},
        {"airline": "Alaska Airlines", "price": 882, "is_nonstop": 0, "duration_mins": dur("2026-07-04T19:35:00", "2026-07-04T19:16:00")+24*60},
        {"airline": "Alaska Airlines", "price": 882, "is_nonstop": 0, "duration_mins": dur("2026-07-04T19:35:00", "2026-07-04T21:34:00")+24*60},
    ]),
    ("ICN-HNL", "2026-12-20", [
        {"airline": "Perimeter Aviation", "price": 593, "is_nonstop": 1, "duration_mins": 500},
        {"airline": "Korean Air", "price": 645, "is_nonstop": 0, "duration_mins": dur("2026-12-20T08:50:00", "2026-12-20T09:20:00")+24*60},
        {"airline": "Korean Air", "price": 645, "is_nonstop": 0, "duration_mins": dur("2026-12-20T15:10:00", "2026-12-20T09:20:00")+24*60},
    ]),
    ("ICN-HNL", "2027-01-15", [
        {"airline": "Perimeter Aviation", "price": 558, "is_nonstop": 1, "duration_mins": 500},
        {"airline": "Korean Air", "price": 705, "is_nonstop": 0, "duration_mins": dur("2027-01-15T09:55:00", "2027-01-15T08:20:00")+24*60},
        {"airline": "Korean Air", "price": 705, "is_nonstop": 0, "duration_mins": dur("2027-01-15T09:55:00", "2027-01-15T09:35:00")+24*60},
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
