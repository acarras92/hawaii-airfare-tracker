#!/usr/bin/env python3
"""
Build the dashboard: regenerate latest.json from DB, embed data into
docs/index.html so it works on GitHub Pages AND when opened locally.
"""

import json
import shutil
import sqlite3
from pathlib import Path

ROOT = Path(__file__).parent
DB_PATH = ROOT / "data" / "prices.db"
JSON_SRC = ROOT / "data" / "latest.json"
JSON_DST = ROOT / "docs" / "latest.json"
HTML_TEMPLATE = ROOT / "docs" / "index.html"

EMBED_MARKER = "// __DATA_EMBED__"


def regenerate_json(conn):
    """Regenerate latest.json from database."""
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


def embed_data_in_html(data):
    """Inject DATA_EMBED into the HTML so it works without fetch()."""
    html = HTML_TEMPLATE.read_text(encoding="utf-8")

    # Remove any previous embed
    lines = html.split("\n")
    cleaned = []
    skip = False
    for line in lines:
        if EMBED_MARKER + "_START" in line:
            skip = True
            continue
        if EMBED_MARKER + "_END" in line:
            skip = False
            continue
        if not skip:
            cleaned.append(line)
    html = "\n".join(cleaned)

    # Build the embed script
    data_json = json.dumps(data, separators=(",", ":"))
    embed_script = (
        f"{EMBED_MARKER}_START\n"
        f"<script>const DATA_EMBED={data_json};</script>\n"
        f"{EMBED_MARKER}_END"
    )

    # Insert just before the main <script> tag
    html = html.replace("<script>\nlet DATA", f"{embed_script}\n<script>\nlet DATA")

    HTML_TEMPLATE.write_text(html, encoding="utf-8")


def main():
    docs = ROOT / "docs"
    docs.mkdir(parents=True, exist_ok=True)

    data = None
    if DB_PATH.exists():
        conn = sqlite3.connect(DB_PATH)
        data = regenerate_json(conn)
        conn.close()
        n_flights = len(data["flights"])
        n_oil = len(data["oil_prices"])
        print(f"Regenerated latest.json: {n_flights} flights, {n_oil} oil records")
    elif JSON_SRC.exists():
        data = json.loads(JSON_SRC.read_text())
        print("Using existing latest.json")
    else:
        data = {"last_updated": None, "flights": [], "oil_prices": []}
        print("No data found, using empty dataset")

    # Copy latest.json into docs/ (for fetch fallback)
    JSON_SRC.parent.mkdir(parents=True, exist_ok=True)
    with open(JSON_SRC, "w") as f:
        json.dump(data, f, indent=2)
    shutil.copy2(JSON_SRC, JSON_DST)

    # Embed data directly into HTML
    embed_data_in_html(data)
    print(f"Embedded {len(data['flights'])} flights into {HTML_TEMPLATE}")
    print(f"Dashboard ready at {HTML_TEMPLATE}")


if __name__ == "__main__":
    main()
