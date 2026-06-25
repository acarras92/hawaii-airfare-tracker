#!/usr/bin/env python3
"""
verify_collection.py - pass/fail gate for the daily Hawaii collection.

Run after collect_data.py + build_dashboard.py, before commit/push, so a bad or
incomplete dataset can't be pushed unnoticed.

Exit codes:
  0  PASS      - flights complete for every live corridor x target_date AND
                 today's WTI oil price is present.
  2  OIL-ONLY  - no flights today but today's oil is present. Acceptable on a
                 flight-search MCP outage: commit the oil-only update and stop.
  1  FAIL      - today's oil is missing, or flights are present but materially
                 incomplete (some corridor x date combos never landed).

Target dates in the past are excluded automatically (collect_data.py skips them),
so the expected count shrinks as dates roll by. Constants are imported from
collect_data.py so this gate can never drift from what's actually collected.

Usage:  py scripts/verify_collection.py [YYYY-MM-DD]   (date defaults to today)
"""
import json
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from collect_data import CORRIDORS, TARGET_DATES, JSON_PATH

# WTI doesn't print on weekends/holidays, so "fresh" means the latest close is
# within this many days of `today` (covers a 3-day holiday weekend), not == today.
OIL_FRESH_DAYS = 4


def main():
    today = sys.argv[1] if len(sys.argv) > 1 else date.today().isoformat()
    today_d = date.fromisoformat(today)

    data = json.loads(Path(JSON_PATH).read_text(encoding="utf-8"))
    flights = data.get("flights", [])
    oil = data.get("oil_prices", [])

    corridors = ["-".join(c) for c in CORRIDORS]
    live_dates = [d for d in TARGET_DATES if d >= today]
    expected_combos = len(corridors) * len(live_dates)

    todays = [f for f in flights if f.get("observed_date") == today]
    combos_today = {(f["corridor"], f["target_date"]) for f in todays}

    oil_dates = [o["date"] for o in oil if o.get("date")]
    latest_oil = max(oil_dates) if oil_dates else None
    oil_fresh = latest_oil is not None and \
        (today_d - date.fromisoformat(latest_oil)).days <= OIL_FRESH_DAYS

    print(f"[verify] date={today}")
    print(f"[verify] live corridors={len(corridors)} live target_dates={len(live_dates)} "
          f"-> expected combos={expected_combos}")
    print(f"[verify] flight rows today={len(todays)} distinct combos today={len(combos_today)}")
    print(f"[verify] latest oil close={latest_oil} fresh(<= {OIL_FRESH_DAYS}d)={oil_fresh}")

    if not oil_fresh:
        print(f"[verify] FAIL: WTI oil is stale (latest close {latest_oil}); oil pipeline broke.")
        return 1

    if not todays:
        print("[verify] OIL-ONLY: no flights collected today "
              "(flight-search likely down). Oil is current; commit oil-only and stop.")
        return 2

    missing = [f"{c}@{d}" for c in corridors for d in live_dates
               if (c, d) not in combos_today]
    if missing:
        shown = ", ".join(missing[:12]) + (" ..." if len(missing) > 12 else "")
        print(f"[verify] FAIL: {len(missing)} combo(s) missing flights: {shown}")
        return 1

    print(f"[verify] PASS: all {expected_combos} corridor x date combos collected, oil current.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
