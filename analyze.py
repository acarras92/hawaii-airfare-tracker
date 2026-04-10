#!/usr/bin/env python3
"""
Analysis utility for Hawaii Airfare Tracker.
Prints correlation analysis, cheapest fares, and volatility metrics.
"""

import sqlite3
from collections import defaultdict
from pathlib import Path

DB_PATH = Path(__file__).parent / "data" / "prices.db"


def pearson(xs, ys):
    n = len(xs)
    if n < 3:
        return None
    mx, my = sum(xs) / n, sum(ys) / n
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    dx = sum((x - mx) ** 2 for x in xs) ** 0.5
    dy = sum((y - my) ** 2 for y in ys) ** 0.5
    if dx == 0 or dy == 0:
        return None
    return num / (dx * dy)


def moving_avg(values, window=7):
    if len(values) < window:
        return values
    result = []
    for i in range(len(values) - window + 1):
        result.append(sum(values[i:i + window]) / window)
    return result


def analyze_correlation(conn):
    print("=" * 60)
    print("OIL vs. AIRFARE CORRELATION (7-day moving averages)")
    print("=" * 60)

    oil_rows = conn.execute("SELECT date, wti_price FROM oil_prices ORDER BY date").fetchall()
    oil_by_date = {r[0]: r[1] for r in oil_rows}

    corridors = [r[0] for r in conn.execute(
        "SELECT DISTINCT corridor FROM flight_observations ORDER BY corridor"
    ).fetchall()]

    for corridor in corridors:
        rows = conn.execute(
            """SELECT observed_date, MIN(price) as cheapest
               FROM flight_observations
               WHERE corridor = ?
               GROUP BY observed_date
               ORDER BY observed_date""",
            (corridor,),
        ).fetchall()

        dates = [r[0] for r in rows]
        fares = [r[1] for r in rows]
        oils = [oil_by_date[d] for d in dates if d in oil_by_date]

        common_dates = [d for d in dates if d in oil_by_date]
        if len(common_dates) < 3:
            print(f"  {corridor}: insufficient data ({len(common_dates)} days)")
            continue

        common_fares = [dict(zip(dates, fares))[d] for d in common_dates]
        common_oils = [oil_by_date[d] for d in common_dates]

        fare_ma = moving_avg(common_fares)
        oil_ma = moving_avg(common_oils)
        min_len = min(len(fare_ma), len(oil_ma))

        r = pearson(fare_ma[:min_len], oil_ma[:min_len])
        if r is not None:
            strength = "strong" if abs(r) > 0.7 else "moderate" if abs(r) > 0.4 else "weak"
            direction = "positive" if r > 0 else "negative"
            print(f"  {corridor}: r = {r:.3f} ({strength} {direction})")
        else:
            print(f"  {corridor}: not enough data for correlation")


def cheapest_fares(conn):
    print()
    print("=" * 60)
    print("CURRENT CHEAPEST FARE PER CORRIDOR / TARGET DATE")
    print("=" * 60)

    latest_date = conn.execute(
        "SELECT MAX(observed_date) FROM flight_observations"
    ).fetchone()[0]

    if not latest_date:
        print("  No data yet.")
        return

    print(f"  (as of {latest_date})")
    print()
    print(f"  {'Corridor':<10} {'Target Date':<12} {'Airline':<20} {'Price':>8} {'Nonstop':>8}")
    print(f"  {'-'*10} {'-'*12} {'-'*20} {'-'*8} {'-'*8}")

    rows = conn.execute(
        """SELECT corridor, target_date, airline, price, is_nonstop
           FROM flight_observations
           WHERE observed_date = ?
           ORDER BY corridor, target_date, price""",
        (latest_date,),
    ).fetchall()

    seen = set()
    for corridor, target, airline, price, nonstop in rows:
        key = (corridor, target)
        if key in seen:
            continue
        seen.add(key)
        ns = "Yes" if nonstop else "No"
        print(f"  {corridor:<10} {target:<12} {airline:<20} ${price:>7.0f} {ns:>8}")


def volatility(conn):
    print()
    print("=" * 60)
    print("PRICE VOLATILITY BY TARGET DATE")
    print("=" * 60)

    targets = [r[0] for r in conn.execute(
        "SELECT DISTINCT target_date FROM flight_observations ORDER BY target_date"
    ).fetchall()]

    stats = []
    for target in targets:
        rows = conn.execute(
            """SELECT observed_date, MIN(price) as cheapest
               FROM flight_observations
               WHERE target_date = ?
               GROUP BY observed_date
               ORDER BY observed_date""",
            (target,),
        ).fetchall()

        prices = [r[1] for r in rows]
        if len(prices) < 2:
            stats.append((target, len(prices), None, None, None))
            continue

        mean = sum(prices) / len(prices)
        variance = sum((p - mean) ** 2 for p in prices) / len(prices)
        std = variance ** 0.5
        spread = max(prices) - min(prices)
        stats.append((target, len(prices), std, spread, mean))

    stats.sort(key=lambda x: x[2] if x[2] is not None else -1, reverse=True)

    print(f"  {'Target Date':<12} {'Days':>5} {'Std Dev':>10} {'Spread':>10} {'Avg':>10}")
    print(f"  {'-'*12} {'-'*5} {'-'*10} {'-'*10} {'-'*10}")
    for target, days, std, spread, mean in stats:
        if std is not None:
            print(f"  {target:<12} {days:>5} ${std:>9.1f} ${spread:>9.0f} ${mean:>9.0f}")
        else:
            print(f"  {target:<12} {days:>5} {'n/a':>10} {'n/a':>10} {'n/a':>10}")


def main():
    if not DB_PATH.exists():
        print(f"Database not found at {DB_PATH}")
        print("Run collect_data.py first.")
        return

    conn = sqlite3.connect(DB_PATH)
    analyze_correlation(conn)
    cheapest_fares(conn)
    volatility(conn)
    conn.close()


if __name__ == "__main__":
    main()
