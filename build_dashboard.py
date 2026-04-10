#!/usr/bin/env python3
"""
Build the dashboard HTML and copy latest.json into docs/ for GitHub Pages.
Run after collect_data.py.
"""

import json
import shutil
import sqlite3
from pathlib import Path

ROOT = Path(__file__).parent
DB_PATH = ROOT / "data" / "prices.db"
JSON_SRC = ROOT / "data" / "latest.json"
JSON_DST = ROOT / "docs" / "latest.json"
HTML_PATH = ROOT / "docs" / "index.html"


def regenerate_json(conn):
    """Regenerate latest.json from database (in case it's stale)."""
    flights = conn.execute(
        """SELECT observed_date, corridor, target_date, airline, price, is_nonstop, duration_mins
           FROM flight_observations ORDER BY observed_date, corridor, target_date, price"""
    ).fetchall()

    oil = conn.execute(
        "SELECT date, wti_price FROM oil_prices ORDER BY date"
    ).fetchall()

    from datetime import datetime, timezone
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

    JSON_SRC.parent.mkdir(parents=True, exist_ok=True)
    with open(JSON_SRC, "w") as f:
        json.dump(output, f, indent=2)

    return output


def main():
    docs = ROOT / "docs"
    docs.mkdir(parents=True, exist_ok=True)

    if DB_PATH.exists():
        conn = sqlite3.connect(DB_PATH)
        data = regenerate_json(conn)
        conn.close()
        n_flights = len(data["flights"])
        n_oil = len(data["oil_prices"])
        print(f"Regenerated latest.json: {n_flights} flights, {n_oil} oil records")
    else:
        print("No database found, using existing latest.json if available")

    # Copy latest.json into docs/ for GitHub Pages
    if JSON_SRC.exists():
        shutil.copy2(JSON_SRC, JSON_DST)
        print(f"Copied latest.json to {JSON_DST}")
    else:
        # Create empty data file so the dashboard doesn't error
        with open(JSON_DST, "w") as f:
            json.dump({"last_updated": None, "flights": [], "oil_prices": []}, f)
        print("Created empty latest.json placeholder")

    print(f"Dashboard ready at {HTML_PATH}")


if __name__ == "__main__":
    main()
