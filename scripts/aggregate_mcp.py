#!/usr/bin/env python3
"""
Aggregate all saved MCP flight-search tool-results into data/mcp_flights.json.

Scans the Claude Code tool-results directory, identifies each result by the
first flight's departure airport and departure date, filters to the known
Hawaii corridor/target-date grid, and writes data/mcp_flights.json.
"""
import json
from datetime import datetime
from pathlib import Path

CORRIDORS = [
    ("LAX", "HNL"), ("SFO", "HNL"), ("JFK", "HNL"),
    ("SEA", "HNL"), ("LAX", "OGG"), ("SFO", "OGG"),
    ("NRT", "HNL"), ("HND", "HNL"), ("KIX", "HNL"),
    ("ICN", "HNL"),
]
TARGET_DATES = [
    "2026-06-15", "2026-07-04", "2026-07-15", "2026-08-01",
    "2026-09-01", "2026-11-25", "2026-12-20", "2027-01-15",
]
TOP_N = 3

AIRPORT_TO_IATA = {
    "Los Angeles International Airport": "LAX",
    "San Francisco International Airport": "SFO",
    "John F Kennedy International Airport": "JFK",
    "Seattle-Tacoma International Airport": "SEA",
    "Daniel K Inouye International Airport": "HNL",
    "Kahului Airport": "OGG",
    "Narita International Airport": "NRT",
    "Tokyo International Airport": "HND",  # HND is "Tokyo International" (Haneda)
    "Kansai International Airport": "KIX",
    "Incheon International Airport": "ICN",
}

REPO = Path(__file__).resolve().parent.parent
RAW_DIR = REPO / "data" / "mcp_raw"
TOOL_RESULTS = Path(r"C:\Users\acarr\.claude\projects\C--Users-acarr-OneDrive-Documents-Claude-Projects-hawaii-airfare-tracker\602092df-abdd-4523-b3ba-2930c9335411\tool-results")
OUT = REPO / "data" / "mcp_flights.json"


def trip_duration(flight):
    legs = flight.get("legs") or []
    if not legs:
        return None
    try:
        dep = datetime.fromisoformat(legs[0]["departure_time"])
        arr = datetime.fromisoformat(legs[-1]["arrival_time"])
        mins = int((arr - dep).total_seconds() // 60)
        return mins if mins > 0 else None
    except (KeyError, ValueError):
        return None


def extract_top(flights):
    rows = []
    for f in flights:
        price = f.get("price")
        legs = f.get("legs") or []
        if not price or price <= 0 or not legs:
            continue
        rows.append({
            "airline": legs[0].get("airline", "Unknown"),
            "price": price,
            "is_nonstop": 1 if len(legs) == 1 else 0,
            "duration_mins": trip_duration(f),
        })
    rows.sort(key=lambda r: r["price"])
    return rows[:TOP_N]


def identify(data):
    flights = data.get("flights") or []
    for f in flights:
        legs = f.get("legs") or []
        if not legs:
            continue
        dep_airport = legs[0].get("departure_airport", "")
        arr_airport = legs[-1].get("arrival_airport", "")
        dep_date = legs[0].get("departure_time", "")[:10]
        origin = AIRPORT_TO_IATA.get(dep_airport)
        dest = AIRPORT_TO_IATA.get(arr_airport)
        if origin and dest and dep_date:
            return origin, dest, dep_date
    return None, None, None


def collect_sources():
    """Yield (corridor, target_date, data) tuples from all available sources."""
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    seen = set()

    # 1. Already-saved files in data/mcp_raw/<corridor>_<date>.json
    for path in RAW_DIR.glob("*.json"):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        # Parse name: LAX-HNL_2026-06-15.json
        base = path.stem
        if "_" in base:
            corridor, target = base.split("_", 1)
            if target in TARGET_DATES:
                key = (corridor, target)
                if key not in seen:
                    seen.add(key)
                    yield corridor, target, data

    # 2. All tool-results files — identify by airport codes and date
    for path in TOOL_RESULTS.glob("*.txt"):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        if not isinstance(data, dict) or "flights" not in data:
            continue
        origin, dest, target = identify(data)
        if not origin or not dest or target not in TARGET_DATES:
            continue
        corridor = f"{origin}-{dest}"
        if (origin, dest) not in CORRIDORS:
            continue
        key = (corridor, target)
        if key in seen:
            continue
        seen.add(key)
        yield corridor, target, data


def main():
    by_key = {}
    for corridor, target, data in collect_sources():
        fares = extract_top(data.get("flights", []))
        if fares:
            by_key[(corridor, target)] = {
                "corridor": corridor,
                "target_date": target,
                "fares": fares,
            }

    entries = []
    missing = []
    for origin, dest in CORRIDORS:
        corridor = f"{origin}-{dest}"
        for target in TARGET_DATES:
            key = (corridor, target)
            if key in by_key:
                entries.append(by_key[key])
            else:
                missing.append(key)

    OUT.write_text(json.dumps(entries, indent=2), encoding="utf-8")
    print(f"Wrote {len(entries)} entries ({len(entries)}/{len(CORRIDORS)*len(TARGET_DATES)}) to {OUT}")
    if missing:
        print(f"Missing {len(missing)} combos:")
        for k in missing:
            print(f"  {k}")


if __name__ == "__main__":
    main()
