#!/usr/bin/env python3
"""
Hawaii Airfare & Oil Price Data Collector

Usage:
  # MCP mode: read flight data from JSON file (populated by Claude Code MCP)
  python collect_data.py --source file --flights-file data/mcp_flights.json

  # SerpAPI mode: fetch flights directly (for GitHub Actions automation)
  python collect_data.py --source serpapi

Both modes fetch oil data from EIA API (set EIA_API_KEY env var).
"""

import argparse
import json
import os
import sqlite3
import sys
import time
from datetime import date, datetime, timezone
from pathlib import Path

import requests

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

DB_PATH = Path(__file__).parent / "data" / "prices.db"
JSON_PATH = Path(__file__).parent / "data" / "latest.json"
TOP_N = 3


def init_db(conn):
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS flight_observations (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            observed_date TEXT NOT NULL,
            corridor      TEXT NOT NULL,
            target_date   TEXT NOT NULL,
            airline       TEXT NOT NULL,
            price         REAL NOT NULL,
            is_nonstop    INTEGER NOT NULL,
            duration_mins INTEGER,
            created_at    TEXT NOT NULL DEFAULT (datetime('now'))
        );
        CREATE INDEX IF NOT EXISTS idx_flight_obs
            ON flight_observations(observed_date, corridor, target_date);

        CREATE TABLE IF NOT EXISTS oil_prices (
            date      TEXT PRIMARY KEY,
            wti_price REAL NOT NULL
        );
    """)


def already_collected(conn, observed_date, corridor, target_date):
    row = conn.execute(
        "SELECT 1 FROM flight_observations WHERE observed_date=? AND corridor=? AND target_date=?",
        (observed_date, corridor, target_date),
    ).fetchone()
    return row is not None


def store_flights(conn, flights_data, observed_date=None):
    if observed_date is None:
        observed_date = date.today().isoformat()

    count = 0
    for entry in flights_data:
        corridor = entry["corridor"]
        target_date = entry["target_date"]

        if target_date <= date.today().isoformat():
            continue
        if already_collected(conn, observed_date, corridor, target_date):
            continue

        for fare in entry["fares"][:TOP_N]:
            conn.execute(
                """INSERT INTO flight_observations
                   (observed_date, corridor, target_date, airline, price, is_nonstop, duration_mins)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (observed_date, corridor, target_date,
                 fare["airline"], fare["price"], fare["is_nonstop"], fare.get("duration_mins")),
            )
            count += 1

    conn.commit()
    return count


def fetch_flights_serpapi(api_key):
    flights_data = []
    today = date.today().isoformat()

    for origin, dest in CORRIDORS:
        for target in TARGET_DATES:
            if target <= today:
                continue

            corridor = f"{origin}-{dest}"
            print(f"  Fetching {corridor} for {target}...")

            resp = requests.get("https://serpapi.com/search", params={
                "engine": "google_flights",
                "departure_id": origin,
                "arrival_id": dest,
                "outbound_date": target,
                "currency": "USD",
                "hl": "en",
                "type": "2",
                "api_key": api_key,
            })
            resp.raise_for_status()
            data = resp.json()

            fares = []
            for flight_list in [data.get("best_flights", []), data.get("other_flights", [])]:
                for f in flight_list:
                    price = f.get("price")
                    if price is None:
                        continue
                    airlines = [leg.get("airline", "Unknown") for leg in f.get("flights", [])]
                    airline = airlines[0] if airlines else "Unknown"
                    stops = len(f.get("layovers", []))
                    duration = f.get("total_duration")
                    fares.append({
                        "airline": airline,
                        "price": price,
                        "is_nonstop": 1 if stops == 0 else 0,
                        "duration_mins": duration,
                    })

            fares.sort(key=lambda x: x["price"])
            flights_data.append({
                "corridor": corridor,
                "target_date": target,
                "fares": fares[:TOP_N],
            })

            time.sleep(1.5)

    return flights_data


def load_flights_from_file(filepath):
    with open(filepath) as f:
        return json.load(f)


def fetch_oil_price(api_key):
    resp = requests.get("https://api.eia.gov/v2/petroleum/pri/spt/data/", params={
        "api_key": api_key,
        "frequency": "daily",
        "data[0]": "value",
        "facets[series][]": "RWTC",
        "sort[0][column]": "period",
        "sort[0][direction]": "desc",
        "length": "5",
    })
    resp.raise_for_status()
    data = resp.json()

    records = data.get("response", {}).get("data", [])
    if not records:
        print("  Warning: No oil price data returned from EIA")
        return None, None

    latest = records[0]
    return latest["period"], float(latest["value"])


def store_oil(conn, oil_date, wti_price):
    conn.execute(
        "INSERT OR REPLACE INTO oil_prices (date, wti_price) VALUES (?, ?)",
        (oil_date, wti_price),
    )
    conn.commit()


def export_json(conn):
    flights = conn.execute(
        """SELECT observed_date, corridor, target_date, airline, price, is_nonstop, duration_mins
           FROM flight_observations ORDER BY observed_date, corridor, target_date, price"""
    ).fetchall()

    oil = conn.execute(
        "SELECT date, wti_price FROM oil_prices ORDER BY date"
    ).fetchall()

    output = {
        "last_updated": datetime.now(timezone.utc).isoformat(),
        "flights": [
            {
                "observed_date": r[0], "corridor": r[1], "target_date": r[2],
                "airline": r[3], "price": r[4], "is_nonstop": r[5], "duration_mins": r[6],
            }
            for r in flights
        ],
        "oil_prices": [{"date": r[0], "wti_price": r[1]} for r in oil],
    }

    JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(JSON_PATH, "w") as f:
        json.dump(output, f, indent=2)

    return len(flights), len(oil)


def main():
    parser = argparse.ArgumentParser(description="Collect Hawaii airfare and oil price data")
    parser.add_argument("--source", choices=["file", "serpapi"], default="file",
                        help="Flight data source: 'file' for MCP-collected JSON, 'serpapi' for API")
    parser.add_argument("--flights-file", default="data/mcp_flights.json",
                        help="Path to MCP-collected flights JSON (used with --source file)")
    parser.add_argument("--skip-oil", action="store_true", help="Skip oil price collection")
    parser.add_argument("--oil-only", action="store_true",
                        help="Only collect oil prices (skip flights). For daily GH Actions.")
    args = parser.parse_args()

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    init_db(conn)

    # Collect flights (unless oil-only mode)
    if not args.oil_only:
        print("Collecting flight data...")
        if args.source == "serpapi":
            api_key = os.environ.get("SERPAPI_KEY")
            if not api_key:
                print("Error: SERPAPI_KEY environment variable not set")
                sys.exit(1)
            flights_data = fetch_flights_serpapi(api_key)
        else:
            flights_file = Path(args.flights_file)
            if not flights_file.exists():
                print(f"Error: Flights file not found: {flights_file}")
                print("Run flight collection via Claude Code MCP first.")
                sys.exit(1)
            flights_data = load_flights_from_file(flights_file)

        flight_count = store_flights(conn, flights_data)
        print(f"  Stored {flight_count} flight observations")
    else:
        print("Oil-only mode — skipping flight collection")

    # Collect oil data
    if not args.skip_oil:
        print("Collecting oil price data...")
        eia_key = os.environ.get("EIA_API_KEY")
        if not eia_key:
            print("  Warning: EIA_API_KEY not set, skipping oil data")
        else:
            oil_date, wti_price = fetch_oil_price(eia_key)
            if oil_date:
                store_oil(conn, oil_date, wti_price)
                print(f"  WTI = ${wti_price:.2f} ({oil_date})")

    # Export JSON
    print("Exporting data...")
    n_flights, n_oil = export_json(conn)
    print(f"  Exported {n_flights} flight records, {n_oil} oil records to {JSON_PATH}")

    conn.close()
    print("Done!")


if __name__ == "__main__":
    main()
