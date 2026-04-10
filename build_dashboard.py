#!/usr/bin/env python3
"""
Build the dashboard: regenerate data from DB, then write a fully
self-contained docs/index.html with all data baked in as a JS const.
No fetch(), no async, no embed magic.
"""

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).parent
DB_PATH = ROOT / "data" / "prices.db"
JSON_PATH = ROOT / "data" / "latest.json"
HTML_PATH = ROOT / "docs" / "index.html"


def load_data():
    """Load data from DB, or fall back to latest.json."""
    if DB_PATH.exists():
        conn = sqlite3.connect(DB_PATH)
        flights = conn.execute(
            """SELECT observed_date, corridor, target_date, airline,
                      price, is_nonstop, duration_mins
               FROM flight_observations
               ORDER BY observed_date, corridor, target_date, price"""
        ).fetchall()
        oil = conn.execute(
            "SELECT date, wti_price FROM oil_prices ORDER BY date"
        ).fetchall()
        conn.close()

        data = {
            "last_updated": datetime.now(timezone.utc).isoformat(),
            "flights": [
                {"observed_date": r[0], "corridor": r[1], "target_date": r[2],
                 "airline": r[3], "price": r[4], "is_nonstop": r[5],
                 "duration_mins": r[6]}
                for r in flights
            ],
            "oil_prices": [{"date": r[0], "wti_price": r[1]} for r in oil],
        }
    elif JSON_PATH.exists():
        data = json.loads(JSON_PATH.read_text())
    else:
        data = {"last_updated": None, "flights": [], "oil_prices": []}

    # Always write latest.json too (for reference / GH Actions)
    JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(JSON_PATH, "w") as f:
        json.dump(data, f, indent=2)

    return data


def build_html(data):
    data_json = json.dumps(data, separators=(",", ":"))
    n_flights = len(data["flights"])
    n_oil = len(data["oil_prices"])

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Hawaii Airfare vs Oil Price Tracker</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.4/chart.umd.min.js"></script>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#0f0f1a;color:#e0e0e0;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,monospace;padding:20px}}
h1{{color:#00d4ff;font-size:1.6em;margin-bottom:4px}}
.sub{{color:#888;font-size:.85em;margin-bottom:16px}}
.controls{{display:flex;flex-wrap:wrap;gap:12px;align-items:center;padding:12px 16px;background:#1a1a2e;border-radius:8px;margin-bottom:16px}}
.controls label{{color:#aaa;font-size:.8em}}
.controls select{{background:#252540;color:#e0e0e0;border:1px solid #333;padding:4px 8px;border-radius:4px;font-size:.85em}}
.checks{{display:flex;flex-wrap:wrap;gap:8px}}
.checks label{{display:flex;align-items:center;gap:4px;background:#252540;padding:2px 8px;border-radius:4px;cursor:pointer}}
.tabs{{display:flex;gap:0;border-bottom:2px solid #252540;flex-wrap:wrap}}
.tab{{padding:8px 20px;cursor:pointer;border:none;background:#1a1a2e;color:#888;font-size:.85em;border-radius:6px 6px 0 0}}
.tab.active{{background:#252540;color:#00d4ff}}
.tab:hover{{color:#00d4ff}}
.pane{{display:none;background:#252540;padding:20px;border-radius:0 0 8px 8px}}
.pane.active{{display:block}}
.chart-box{{position:relative;height:420px;margin:8px 0}}
table{{width:100%;border-collapse:collapse;font-size:.85em;margin-top:8px}}
th{{text-align:left;padding:8px 12px;border-bottom:2px solid #333;color:#00d4ff;cursor:pointer;user-select:none}}
th:hover{{color:#fff}}
td{{padding:6px 12px;border-bottom:1px solid #1a1a2e}}
tr:hover td{{background:#1a1a2e}}
.card{{background:#1a1a2e;border-radius:8px;padding:16px;margin-bottom:12px;border:1px solid #252540}}
.card h3{{color:#00d4ff;font-size:.95em;margin-bottom:8px;border-bottom:1px solid #333;padding-bottom:6px}}
.card p,.card li{{font-size:.85em;line-height:1.6;color:#bbb}}
.card ul{{list-style:none;padding:0}}
.card li{{padding:4px 0;border-bottom:1px solid #252540}}
.card li:last-child{{border-bottom:none}}
.accent{{color:#00d4ff;font-weight:600}}
.green{{color:#4cff8e}}
.red{{color:#ff6b6b}}
.dim{{color:#666}}
.info-box{{background:#0f0f1a;border-radius:6px;padding:12px 16px;margin:8px 0;font-size:.85em;color:#aaa;border-left:3px solid #00d4ff}}
#updated{{color:#666;font-size:.75em}}
</style>
</head>
<body>

<h1>Hawaii Airfare vs. Oil Price Tracker</h1>
<p class="sub">Daily tracking of airfares into Hawaii correlated with WTI crude oil prices</p>

<div class="controls">
  <div>
    <label>Target Date</label><br>
    <select id="targetSel"></select>
  </div>
  <div>
    <label>Corridors</label><br>
    <div class="checks" id="corrChecks"></div>
  </div>
  <div id="updated"></div>
</div>

<div class="tabs" id="tabBar"></div>
<div id="panes"></div>

<script>
const DATA = {data_json};

const COLORS = ['#00d4ff','#ff6b6b','#4cff8e','#ffd93d','#c084fc','#f97316','#22d3ee','#e879f9'];
const TAB_NAMES = ['Oil vs Airfare','By Corridor','Booking Snapshot','Airline Breakdown','Analysis & Insights'];

// ---- helpers ----
function unique(arr) {{ return [...new Set(arr)].sort(); }}
function targetDates() {{ return unique(DATA.flights.map(f=>f.target_date)); }}
function corridors()   {{ return unique(DATA.flights.map(f=>f.corridor)); }}
function obsDates()    {{ return unique(DATA.flights.map(f=>f.observed_date)); }}

function selTarget() {{ return document.getElementById('targetSel').value; }}
function selCorridors() {{
  return [...document.querySelectorAll('#corrChecks input:checked')].map(i=>i.value);
}}

function cheapest(flights) {{
  const m = {{}};
  flights.forEach(f => {{
    const k = f.corridor+'|'+f.target_date;
    if (!m[k] || f.price < m[k].price) m[k] = f;
  }});
  return Object.values(m);
}}

// ---- build controls ----
function initControls() {{
  const sel = document.getElementById('targetSel');
  targetDates().forEach(d => {{
    const o = document.createElement('option');
    o.value = d; o.textContent = d; sel.appendChild(o);
  }});
  sel.onchange = renderActive;

  const box = document.getElementById('corrChecks');
  corridors().forEach(c => {{
    const lbl = document.createElement('label');
    lbl.innerHTML = '<input type="checkbox" value="'+c+'" checked> '+c;
    lbl.querySelector('input').onchange = renderActive;
    box.appendChild(lbl);
  }});

  if (DATA.last_updated) {{
    document.getElementById('updated').textContent =
      'Updated: ' + new Date(DATA.last_updated).toLocaleString();
  }}
}}

// ---- tabs ----
let activeTab = 0;
function buildTabs() {{
  const bar = document.getElementById('tabBar');
  const panes = document.getElementById('panes');
  TAB_NAMES.forEach((name, i) => {{
    const btn = document.createElement('button');
    btn.className = 'tab' + (i===0?' active':'');
    btn.textContent = name;
    btn.onclick = () => {{
      document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'));
      document.querySelectorAll('.pane').forEach(p=>p.classList.remove('active'));
      btn.classList.add('active');
      document.getElementById('pane'+i).classList.add('active');
      activeTab = i;
      renderActive();
    }};
    bar.appendChild(btn);

    const div = document.createElement('div');
    div.className = 'pane' + (i===0?' active':'');
    div.id = 'pane'+i;
    panes.appendChild(div);
  }});
}}

// ---- chart instances ----
let charts = {{}};
function clearChart(id) {{
  if (charts[id]) {{ charts[id].destroy(); delete charts[id]; }}
}}

function renderActive() {{
  const fns = [renderTab0, renderTab1, renderTab2, renderTab3, renderTab4];
  fns[activeTab]();
}}

// ======== TAB 0: Oil vs Airfare ========
function renderTab0() {{
  const pane = document.getElementById('pane0');
  const dates = obsDates();
  if (dates.length < 3) {{
    pane.innerHTML =
      '<div class="card"><h3>Building Data</h3>' +
      '<p><span class="accent">' + dates.length + ' day(s)</span> of data collected so far. ' +
      'Correlation chart available after <span class="accent">7+ days</span> of daily observations.</p>' +
      '<div class="info-box">Keep running daily flight collection to build the time series. ' +
      'Oil data updates automatically via GitHub Actions.</div></div>' +
      '<div class="card"><h3>Data Collected So Far</h3>' +
      '<p>Flights: <span class="accent">' + DATA.flights.length + '</span> observations across ' +
      '<span class="accent">' + corridors().length + '</span> corridors and ' +
      '<span class="accent">' + targetDates().length + '</span> target dates</p>' +
      '<p>Oil: WTI at <span class="accent">$' +
      (DATA.oil_prices.length ? DATA.oil_prices[DATA.oil_prices.length-1].wti_price.toFixed(2) : '---') +
      '/bbl</span>' +
      (DATA.oil_prices.length ? ' (' + DATA.oil_prices[DATA.oil_prices.length-1].date + ')' : '') +
      '</p></div>';
    return;
  }}
  // With enough data, show dual-axis chart
  const target = selTarget();
  const corrs = selCorridors();
  const filtered = DATA.flights.filter(f =>
    f.target_date === target && corrs.includes(f.corridor));
  const fareByDate = {{}};
  filtered.forEach(f => {{
    if (!fareByDate[f.observed_date] || f.price < fareByDate[f.observed_date])
      fareByDate[f.observed_date] = f.price;
  }});
  const oilByDate = {{}};
  DATA.oil_prices.forEach(o => {{ oilByDate[o.date] = o.wti_price; }});
  const allDates = unique([...Object.keys(fareByDate), ...Object.keys(oilByDate)]);

  pane.innerHTML = '<div class="chart-box"><canvas id="c0"></canvas></div>';
  clearChart('c0');
  charts['c0'] = new Chart(document.getElementById('c0'), {{
    type:'line',
    data:{{
      labels: allDates,
      datasets:[
        {{label:'Cheapest Fare ($)',data:allDates.map(d=>fareByDate[d]??null),
          borderColor:'#00d4ff',yAxisID:'y',tension:.3,pointRadius:2,spanGaps:true}},
        {{label:'WTI Crude ($/bbl)',data:allDates.map(d=>oilByDate[d]??null),
          borderColor:'#ff6b6b',yAxisID:'y1',tension:.3,pointRadius:2,spanGaps:true}}
      ]
    }},
    options:{{
      responsive:true,maintainAspectRatio:false,
      plugins:{{legend:{{labels:{{color:'#ccc'}}}}}},
      scales:{{
        x:{{ticks:{{color:'#888',maxTicksLimit:15}},grid:{{color:'#1a1a2e'}}}},
        y:{{position:'left',title:{{display:true,text:'Fare ($)',color:'#00d4ff'}},
            ticks:{{color:'#00d4ff'}},grid:{{color:'#1a1a2e'}}}},
        y1:{{position:'right',title:{{display:true,text:'WTI ($/bbl)',color:'#ff6b6b'}},
             ticks:{{color:'#ff6b6b'}},grid:{{drawOnChartArea:false}}}}
      }}
    }}
  }});
}}

// ======== TAB 1: By Corridor ========
function renderTab1() {{
  const pane = document.getElementById('pane1');
  const target = selTarget();
  const corrs = selCorridors();
  const filtered = DATA.flights.filter(f =>
    f.target_date === target && corrs.includes(f.corridor));

  // Cheapest per corridor per date
  const byCorridor = {{}};
  filtered.forEach(f => {{
    if (!byCorridor[f.corridor]) byCorridor[f.corridor] = {{}};
    if (!byCorridor[f.corridor][f.observed_date] || f.price < byCorridor[f.corridor][f.observed_date])
      byCorridor[f.corridor][f.observed_date] = f.price;
  }});
  const dates = unique(filtered.map(f=>f.observed_date));
  const useBar = dates.length < 3;
  const corrKeys = Object.keys(byCorridor).sort();

  pane.innerHTML = '<div class="chart-box"><canvas id="c1"></canvas></div>';
  clearChart('c1');

  if (useBar) {{
    charts['c1'] = new Chart(document.getElementById('c1'), {{
      type:'bar',
      data:{{
        labels: corrKeys,
        datasets: dates.map((d,i) => ({{
          label: d,
          data: corrKeys.map(c => byCorridor[c][d] ?? null),
          backgroundColor: COLORS[i % COLORS.length] + '99',
          borderColor: COLORS[i % COLORS.length],
          borderWidth: 1
        }}))
      }},
      options:{{
        responsive:true,maintainAspectRatio:false,
        plugins:{{legend:{{labels:{{color:'#ccc'}}}},
                  title:{{display:true,text:'Cheapest fare for '+target,color:'#ccc'}}}},
        scales:{{
          x:{{ticks:{{color:'#888'}},grid:{{color:'#1a1a2e'}}}},
          y:{{title:{{display:true,text:'Price ($)',color:'#ccc'}},
              ticks:{{color:'#ccc'}},grid:{{color:'#1a1a2e'}}}}
        }}
      }}
    }});
  }} else {{
    charts['c1'] = new Chart(document.getElementById('c1'), {{
      type:'line',
      data:{{
        labels: dates,
        datasets: corrKeys.map((c,i) => ({{
          label:c,
          data: dates.map(d => byCorridor[c][d] ?? null),
          borderColor: COLORS[i%COLORS.length],
          tension:.3,pointRadius:2,spanGaps:true
        }}))
      }},
      options:{{
        responsive:true,maintainAspectRatio:false,
        plugins:{{legend:{{labels:{{color:'#ccc'}}}}}},
        scales:{{
          x:{{ticks:{{color:'#888',maxTicksLimit:15}},grid:{{color:'#1a1a2e'}}}},
          y:{{title:{{display:true,text:'Cheapest Fare ($)',color:'#ccc'}},
              ticks:{{color:'#ccc'}},grid:{{color:'#1a1a2e'}}}}
        }}
      }}
    }});
  }}
}}

// ======== TAB 2: Booking Snapshot ========
function renderTab2() {{
  const pane = document.getElementById('pane2');
  const corrs = selCorridors();
  const latest = obsDates().slice(-1)[0];
  if (!latest) {{ pane.innerHTML = '<p class="dim">No data yet.</p>'; return; }}

  const todayFlights = DATA.flights.filter(f => f.observed_date === latest && corrs.includes(f.corridor));
  const targets = targetDates();

  // Cheapest per corridor per target
  const byCorridor = {{}};
  todayFlights.forEach(f => {{
    if (!byCorridor[f.corridor]) byCorridor[f.corridor] = {{}};
    if (!byCorridor[f.corridor][f.target_date] || f.price < byCorridor[f.corridor][f.target_date])
      byCorridor[f.corridor][f.target_date] = f.price;
  }});
  const corrKeys = Object.keys(byCorridor).sort();

  pane.innerHTML = '<div class="chart-box" style="height:500px"><canvas id="c2"></canvas></div>';
  clearChart('c2');
  charts['c2'] = new Chart(document.getElementById('c2'), {{
    type:'bar',
    data:{{
      labels: targets,
      datasets: corrKeys.map((c,i) => ({{
        label: c,
        data: targets.map(t => byCorridor[c]?.[t] ?? null),
        backgroundColor: COLORS[i%COLORS.length] + '99',
        borderColor: COLORS[i%COLORS.length],
        borderWidth: 1
      }}))
    }},
    options:{{
      responsive:true,maintainAspectRatio:false,
      plugins:{{
        legend:{{labels:{{color:'#ccc'}}}},
        title:{{display:true,text:'Forward Booking Snapshot ('+latest+')',color:'#ccc'}}
      }},
      scales:{{
        x:{{ticks:{{color:'#888'}},grid:{{color:'#1a1a2e'}}}},
        y:{{title:{{display:true,text:'Price ($)',color:'#ccc'}},
            ticks:{{color:'#ccc'}},grid:{{color:'#1a1a2e'}}}}
      }}
    }}
  }});
}}

// ======== TAB 3: Airline Breakdown ========
function renderTab3() {{
  const pane = document.getElementById('pane3');
  const latest = obsDates().slice(-1)[0];
  if (!latest) {{ pane.innerHTML = '<p class="dim">No data yet.</p>'; return; }}

  const rows = DATA.flights
    .filter(f => f.observed_date === latest)
    .sort((a,b) => a.corridor.localeCompare(b.corridor) || a.price - b.price);

  let html = '<table><thead><tr>' +
    '<th>Corridor</th><th>Target Date</th><th>Airline</th><th>Price</th><th>Nonstop</th>' +
    '</tr></thead><tbody>';
  rows.forEach(r => {{
    const ns = r.is_nonstop ? '<span class="green">Yes</span>' : '<span class="dim">No</span>';
    html += '<tr><td>'+r.corridor+'</td><td>'+r.target_date+'</td><td>'+r.airline+
            '</td><td>$'+r.price.toFixed(0)+'</td><td>'+ns+'</td></tr>';
  }});
  html += '</tbody></table>';
  html += '<p class="dim" style="margin-top:8px">'+rows.length+' observations from '+latest+'</p>';
  pane.innerHTML = html;

  // Sortable headers
  pane.querySelectorAll('th').forEach((th, idx) => {{
    th.onclick = () => {{
      const tbody = pane.querySelector('tbody');
      const trs = [...tbody.querySelectorAll('tr')];
      const dir = th.dataset.dir === 'asc' ? 'desc' : 'asc';
      th.dataset.dir = dir;
      trs.sort((a,b) => {{
        let av = a.children[idx].textContent;
        let bv = b.children[idx].textContent;
        if (idx === 3) {{ av = parseFloat(av.replace('$','')); bv = parseFloat(bv.replace('$','')); }}
        if (av < bv) return dir === 'asc' ? -1 : 1;
        if (av > bv) return dir === 'asc' ? 1 : -1;
        return 0;
      }});
      trs.forEach(r => tbody.appendChild(r));
    }};
  }});
}}

// ======== TAB 4: Analysis & Insights ========
function renderTab4() {{
  const pane = document.getElementById('pane4');
  const latest = obsDates().slice(-1)[0];
  if (!latest) {{ pane.innerHTML = '<p class="dim">No data yet.</p>'; return; }}

  const todayFlights = DATA.flights.filter(f => f.observed_date === latest);
  const ch = cheapest(todayFlights);

  // Cheapest overall
  const cheapestAll = ch.reduce((best, f) => (!best || f.price < best.price) ? f : best, null);

  // Most expensive
  const mostExpensive = ch.reduce((best, f) => (!best || f.price > best.price) ? f : best, null);

  // Sep 1 baseline vs Dec 20 premium
  const sep = ch.filter(f => f.target_date === '2026-09-01');
  const dec = ch.filter(f => f.target_date === '2026-12-20');
  let premiumHtml = '';
  if (sep.length && dec.length) {{
    const sepAvg = sep.reduce((s,f)=>s+f.price,0) / sep.length;
    const decAvg = dec.reduce((s,f)=>s+f.price,0) / dec.length;
    const pct = ((decAvg - sepAvg) / sepAvg * 100).toFixed(0);
    premiumHtml = '<li>Holiday premium: Dec 20 averages <span class="accent">$' +
      decAvg.toFixed(0) + '</span> vs Sep 1 baseline <span class="accent">$' +
      sepAvg.toFixed(0) + '</span> &mdash; <span class="red">+' + pct + '% markup</span></li>';
  }}

  // Oil price
  const oilLatest = DATA.oil_prices.length
    ? DATA.oil_prices[DATA.oil_prices.length - 1] : null;

  let html = '<div class="card"><h3>Key Findings ('+latest+')</h3><ul>';

  if (cheapestAll) {{
    html += '<li>Cheapest route today: <span class="accent">' + cheapestAll.corridor +
            '</span> on ' + cheapestAll.target_date +
            ' &mdash; <span class="green">$' + cheapestAll.price.toFixed(0) + '</span>' +
            ' (' + cheapestAll.airline + (cheapestAll.is_nonstop ? ', nonstop' : '') + ')</li>';
  }}
  if (mostExpensive) {{
    html += '<li>Most expensive: <span class="accent">' + mostExpensive.corridor +
            '</span> on ' + mostExpensive.target_date +
            ' &mdash; <span class="red">$' + mostExpensive.price.toFixed(0) + '</span>' +
            ' (' + mostExpensive.airline + ')</li>';
  }}
  html += premiumHtml;

  if (oilLatest) {{
    html += '<li>WTI crude oil: <span class="accent">$' + oilLatest.wti_price.toFixed(2) +
            '/bbl</span> (' + oilLatest.date + ')</li>';
  }}

  html += '</ul></div>';

  // Corridor summary
  html += '<div class="card"><h3>Cheapest Fare by Corridor</h3><table>' +
    '<thead><tr><th>Corridor</th><th>Best Target Date</th><th>Price</th><th>Airline</th></tr></thead><tbody>';
  const byCorr = {{}};
  ch.forEach(f => {{
    if (!byCorr[f.corridor] || f.price < byCorr[f.corridor].price)
      byCorr[f.corridor] = f;
  }});
  Object.keys(byCorr).sort().forEach(c => {{
    const f = byCorr[c];
    html += '<tr><td>'+c+'</td><td>'+f.target_date+'</td><td class="green">$'+
            f.price.toFixed(0)+'</td><td>'+f.airline+'</td></tr>';
  }});
  html += '</tbody></table></div>';

  // Correlation note
  const nDays = obsDates().length;
  html += '<div class="info-box">Correlation analysis begins after 7 days of data. ' +
    'Currently tracking <span class="accent">' + nDays + ' day(s)</span>. ' +
    'Oil and airfare trends will be compared once enough daily observations exist.</div>';

  pane.innerHTML = html;
}}

// ---- init ----
document.addEventListener('DOMContentLoaded', function() {{
  initControls();
  buildTabs();
  renderActive();
}});
</script>
</body>
</html>"""

    return html


def main():
    docs = ROOT / "docs"
    docs.mkdir(parents=True, exist_ok=True)

    data = load_data()
    n_flights = len(data["flights"])
    n_oil = len(data["oil_prices"])
    print(f"Data: {n_flights} flights, {n_oil} oil records")

    html = build_html(data)
    HTML_PATH.write_text(html, encoding="utf-8")
    print(f"Wrote {HTML_PATH} ({len(html)} bytes)")

    # Also copy latest.json to docs/ for reference
    import shutil
    shutil.copy2(JSON_PATH, docs / "latest.json")
    print("Done")


if __name__ == "__main__":
    main()
