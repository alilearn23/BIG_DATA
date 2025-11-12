import os, sys, subprocess
from flask import Flask, send_from_directory, render_template_string

APP = Flask(__name__)
BASE = os.getcwd()
FIG = os.path.join(BASE, "figures")
OUT = os.path.join(BASE, "output")
RPT = os.path.join(BASE, "report")
os.makedirs(OUT, exist_ok=True)

# Try to (re)run analysis so figures/ & cleaned CSV are fresh
if os.path.exists(os.path.join(BASE, "TP03_analysis.py")):
    try:
        subprocess.call([sys.executable, "TP03_analysis.py"])
    except Exception as e:
        print("Analysis error:", e)

INDEX = """
<!doctype html>
<html><head><meta charset="utf-8"><title>TP04 Results</title></head>
<body>
  <h1>TP04 — Dockerized TP03 Results</h1>
  <h2>Figures</h2>
  <ul>
    <li><a href="/fig/sales_over_time.png">sales_over_time.png</a></li>
    <li><a href="/fig/top_products.png">top_products.png</a></li>
    <li><a href="/fig/revenue_by_region.png">revenue_by_region.png</a></li>
    <li><a href="/fig/customer_segments.png">customer_segments.png</a></li>
  </ul>
  <h2>Data</h2>
  <ul>
    <li><a href="/file/TP03_sales_data_clean.csv">TP03_sales_data_clean.csv</a></li>
    <li><a href="/file/customer_segments.csv">customer_segments.csv</a></li>
  </ul>
  <h2>Power BI</h2>
  <p>Download the PBIX file:</p>
  <ul>
    <li><a href="/report/PowerBI_Sales_Dashboard.pbix">PowerBI_Sales_Dashboard.pbix</a></li>
  </ul>
</body></html>
"""

@APP.route("/")
def index():
    return render_template_string(INDEX)

@APP.route("/fig/<path:name>")
def fig(name):
    return send_from_directory(FIG, name, as_attachment=False)

@APP.route("/file/<path:name>")
def file(name):
    return send_from_directory(BASE, name, as_attachment=True)

@APP.route("/report/<path:name>")
def report(name):
    return send_from_directory(RPT, name, as_attachment=True)

if __name__ == "__main__":
    APP.run(host="0.0.0.0", port=80)
