# -*- coding: utf-8 -*-
"""
Smart Farming Profit Calculator - Flask App
============================================

A simple Flask web app for our Simulation Lab project.

WHAT THIS APP DOES:
1. MATRIX MULTIPLICATION  (lab task)
   3x3 yield matrix x 3x1 price vector = revenue per land
2. STATISTICS              (lab task)
   Mean, Median, Std Dev, Range of revenues
3. VISUALIZATION           (lab task)
   Heatmap of yield matrix + Bar chart of revenues
4. T-TEST (A/B Testing)    (lab task)
   Test if new organic fertilizer beats traditional one
5. WEATHER SIMULATION      (innovative)
   Normal / Good Rain / Drought / Flood effect on yield
6. RISK LEVEL              (innovative)
   Low / Medium / High based on standard deviation
7. COST & PROFIT           (innovative)
   Subtract seed+fertilizer+labor cost from revenue
8. CROP RECOMMENDATION     (smart)
   Suggest best crop for each land
9. SAVE HISTORY            (smart)
   Save calculations to SQLite, view them later
10. EXPORT CSV             (smart)
    Download the result as a CSV file
11. BILINGUAL              (smart)
    Toggle between English and Bangla

HOW TO RUN (in VS Code):
    1. Open this folder in VS Code.
    2. Open Terminal and run:  pip install -r requirements.txt
    3. Then run:  python app.py
    4. Open browser at: http://127.0.0.1:5000
"""

# ===== Step 1: Import the libraries we need =====
import os
import csv
import io
import json
import sqlite3
from datetime import datetime

from flask import (Flask, render_template, request, session,
                   redirect, url_for, Response, flash)
import numpy as np
from scipy import stats

from translations import get_text

# ===== Step 2: Create the Flask app =====
app = Flask(__name__)
app.secret_key = "smart_farming_2024"

# Path to the SQLite database file
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "farming.db")

# Names of lands and crops (only 3 each - same as our lab work)
LANDS = ["Land 1", "Land 2", "Land 3"]
CROPS = ["Rice", "Wheat", "Corn"]


# ============================================================
# DATABASE FUNCTIONS (only 4 small functions)
# ============================================================

def init_db():
    """Create the database table if it does not exist. Runs once at start."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS calculations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            yield_matrix TEXT,
            prices TEXT,
            costs TEXT,
            weather TEXT,
            revenue TEXT,
            profit TEXT,
            total_profit REAL,
            best_land TEXT,
            risk TEXT,
            stats TEXT,
            best_crops TEXT
        )
    """)
    conn.commit()
    conn.close()


def save_to_db(data):
    """Save one calculation result into the database."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        INSERT INTO calculations
        (date, yield_matrix, prices, costs, weather, revenue, profit,
         total_profit, best_land, risk, stats, best_crops)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["date"], data["yield_matrix"], data["prices"], data["costs"],
        data["weather"], data["revenue"], data["profit"],
        data["total_profit"], data["best_land"], data["risk"],
        data["stats"], data["best_crops"]
    ))
    conn.commit()
    conn.close()


def get_all_records():
    """Get all saved calculations, newest first."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT * FROM calculations ORDER BY id DESC").fetchall()
    conn.close()
    return rows


def delete_record(record_id):
    """Delete one calculation by its ID."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("DELETE FROM calculations WHERE id = ?", (record_id,))
    conn.commit()
    conn.close()


# ============================================================
# HELPER: get current language and translated text
# ============================================================

def get_lang():
    """Return 'en' or 'bn' based on what the user picked."""
    return session.get("lang", "en")


def t(key):
    """Shortcut: get translated text for the current language."""
    return get_text(key, get_lang())


# ============================================================
# CALCULATION FUNCTIONS
# Each function does ONE small job - so it is easy to explain to mam.
# ============================================================

def apply_weather(yield_matrix, weather):
    """
    WEATHER SIMULATION (innovative feature).

    Multiplies the yield matrix by a factor based on weather:
      - Normal:  1.0  (no change)
      - Good:    1.2  (+20%, favorable rain)
      - Drought: 0.7  (-30%, unfavorable)
      - Flood:   0.5  (-50%, damaging)
    """
    factors = {"normal": 1.0, "good": 1.2, "drought": 0.7, "flood": 0.5}
    factor = factors.get(weather, 1.0)
    return (np.array(yield_matrix, dtype=float) * factor).tolist()


def calculate_revenue(yield_matrix, prices):
    """
    MATRIX MULTIPLICATION (the main math of this project).

    yield_matrix = 3x3 matrix (3 lands x 3 crops), values in kg.
    prices       = 3x1 vector (price per kg for each crop), values in Tk.

    We use numpy.dot() to multiply them.
    The result is a 3x1 vector: total revenue for each land.

    Example:
        yield_matrix = [[1000, 800, 500],   # Land 1
                        [ 900, 700, 600],   # Land 2
                        [1100, 850, 550]]   # Land 3

        prices = [25, 30, 20]   # Rice, Wheat, Corn per kg

        revenue = yield_matrix @ prices
                = [1000*25 + 800*30 + 500*20,    # Land 1
                   900*25 + 700*30 + 600*20,    # Land 2
                   1100*25 + 850*30 + 550*20]   # Land 3
                = [59000, 55500, 63250]
    """
    ym = np.array(yield_matrix, dtype=float)
    pm = np.array(prices, dtype=float)
    revenue = np.dot(ym, pm)   # this is the matrix multiplication
    return revenue.tolist()


def calculate_profit(revenue, costs):
    """COST & PROFIT (innovative). Profit = Revenue - Cost for each land."""
    return [revenue[i] - costs[i] for i in range(len(revenue))]


def calculate_statistics(values):
    """
    STATISTICS: find Mean, Median, Std Dev, and Range of a list of numbers.

    Mean   = sum of values / number of values  (average)
    Median = middle value when sorted
    Std    = standard deviation (how spread out the values are)
    Range  = max value - min value
    """
    arr = np.array(values, dtype=float)
    return {
        "mean":   float(np.mean(arr)),
        "median": float(np.median(arr)),
        "std":    float(np.std(arr)),
        "range":  float(np.ptp(arr)),    # ptp = peak-to-peak = max - min
    }


def find_best_land(profit_list):
    """Find which land gave the highest profit. Return its name."""
    best_index = int(np.argmax(profit_list))
    return LANDS[best_index]


def find_best_crop_per_land(yield_matrix, prices):
    """
    CROP RECOMMENDATION (smart feature).

    For each land, find which crop gave the most revenue.
    Returns a list of crop names (one per land).
    """
    ym = np.array(yield_matrix, dtype=float)
    pm = np.array(prices, dtype=float)
    revenue_per_crop = ym * pm   # revenue for each crop on each land
    best_crops = []
    for i in range(ym.shape[0]):
        best_idx = int(np.argmax(revenue_per_crop[i]))
        best_crops.append(CROPS[best_idx])
    return best_crops


def get_risk_level(std_value):
    """
    RISK LEVEL (innovative feature).

    Uses the standard deviation of profits to decide risk:
      - Std < 1000  -> Low Risk    (stable income across lands)
      - Std < 5000  -> Medium Risk (some variation)
      - else        -> High Risk   (very different income per land)
    """
    if std_value < 1000:
        return "Low Risk"
    elif std_value < 5000:
        return "Medium Risk"
    else:
        return "High Risk"


def run_t_test():
    """
    T-TEST (A/B Testing):

    We want to test if a NEW organic fertilizer gives more yield
    than the TRADITIONAL fertilizer.

    We generate 10 random sample yields for each group:
      - Traditional:  mean = 1200 kg, std = 50
      - Organic:      mean = 1380 kg, std = 60

    Then we run an "independent T-Test" using scipy.
    It gives us:
      - t_stat : how big the difference is
      - p_val  : how likely this difference happened by chance

    Decision rule:
      - If p_val < 0.05  -> the new fertilizer REALLY works (significant)
      - If p_val >= 0.05 -> the difference is NOT significant
    """
    np.random.seed(42)   # same seed so we get same random numbers every time
    traditional = np.random.normal(1200, 50, 10)
    organic = np.random.normal(1380, 60, 10)
    t_stat, p_val = stats.ttest_ind(traditional, organic, equal_var=False)

    return {
        "traditional_mean": float(np.mean(traditional)),
        "organic_mean":     float(np.mean(organic)),
        "t_stat":           float(t_stat),
        "p_val":             float(p_val),
        "significant":       bool(p_val < 0.05),
        "traditional_data":  traditional.tolist(),
        "organic_data":      organic.tolist(),
    }


# ============================================================
# ROUTES (URL handlers)
# ============================================================

@app.route("/")
def index():
    """Main page - shows form and (if available) the result."""
    # NOTE: use session.get (NOT pop) so the result stays in session.
    # This way "Save Result" and "Export CSV" buttons still work after
    # the page is rendered.
    result = session.get("result", None)
    return render_template("index.html",
                           lands=LANDS, crops=CROPS,
                           result=result, t=t, lang=get_lang())


@app.route("/calculate", methods=["POST"])
def calculate():
    """Read the form, do all calculations, save result in session, redirect."""
    # ---- Read the 3x3 yield matrix ----
    yield_matrix = []
    for i in range(3):
        row = []
        for j in range(3):
            value = request.form.get(f"yield_{i}_{j}", type=float) or 0.0
            row.append(value)
        yield_matrix.append(row)

    # ---- Read the 3 prices ----
    prices = [request.form.get(f"price_{j}", type=float) or 0.0 for j in range(3)]

    # ---- Read the 3 costs ----
    costs = [request.form.get(f"cost_{i}", type=float) or 0.0 for i in range(3)]

    # ---- Read the chosen weather ----
    weather = request.form.get("weather", "normal")

    # ---- Apply weather simulation to the yield ----
    weather_yield = apply_weather(yield_matrix, weather)

    # ---- Do all calculations ----
    revenue = calculate_revenue(weather_yield, prices)
    profit = calculate_profit(revenue, costs)
    statistics = calculate_statistics(profit)
    best_land = find_best_land(profit)
    best_crops = find_best_crop_per_land(weather_yield, prices)
    risk = get_risk_level(statistics["std"])
    ttest = run_t_test()

    # ---- Pack everything into one dictionary ----
    result = {
        "yield_matrix":  yield_matrix,
        "weather_yield": weather_yield,
        "weather":       weather,
        "prices":        prices,
        "costs":         costs,
        "revenue":       revenue,
        "profit":        profit,
        "statistics":    statistics,
        "best_land":     best_land,
        "best_crops":    best_crops,
        "risk":          risk,
        "ttest":         ttest,
        "date":          datetime.now().strftime("%Y-%m-%d %H:%M"),
    }

    session["result"] = result
    return redirect(url_for("index"))


@app.route("/save", methods=["POST"])
def save():
    """Save the last calculated result to the SQLite database."""
    result = session.get("result")
    if not result:
        flash(t("msg_no_data"))
        return redirect(url_for("index"))

    data = {
        "date":          result["date"],
        "yield_matrix":  json.dumps(result["yield_matrix"]),
        "prices":        json.dumps(result["prices"]),
        "costs":         json.dumps(result["costs"]),
        "weather":       result["weather"],
        "revenue":       json.dumps(result["revenue"]),
        "profit":        json.dumps(result["profit"]),
        "total_profit":  result["statistics"]["total"] if "total" in result["statistics"] else float(np.sum(result["profit"])),
        "best_land":     result["best_land"],
        "risk":          result["risk"],
        "stats":         json.dumps(result["statistics"]),
        "best_crops":    json.dumps(result["best_crops"]),
    }
    save_to_db(data)
    flash(t("msg_saved"))
    return redirect(url_for("history"))


@app.route("/history")
def history():
    """Show all saved calculations."""
    records = get_all_records()
    return render_template("history.html", records=records, t=t, lang=get_lang())


@app.route("/history/<int:record_id>/delete", methods=["POST"])
def delete(record_id):
    """Delete a saved calculation."""
    delete_record(record_id)
    flash(t("msg_deleted"))
    return redirect(url_for("history"))


@app.route("/export_csv")
def export_csv():
    """Export the last calculated result as a CSV file download."""
    result = session.get("result")
    if not result:
        flash(t("msg_no_data"))
        return redirect(url_for("index"))

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow(["Smart Farming Profit Calculator - CSV Export"])
    writer.writerow(["Date", result["date"]])
    writer.writerow([])

    writer.writerow(["Yield Matrix (kg) - Weather: " + result["weather"]])
    writer.writerow(["Land"] + CROPS)
    for i, land in enumerate(LANDS):
        writer.writerow([land] + result["weather_yield"][i])
    writer.writerow([])

    writer.writerow(["Prices per kg (Tk)"])
    writer.writerow(CROPS)
    writer.writerow(result["prices"])
    writer.writerow([])

    writer.writerow(["Cost per Land (Tk)"])
    writer.writerow(LANDS)
    writer.writerow(result["costs"])
    writer.writerow([])

    writer.writerow(["Revenue & Profit per Land (Tk)"])
    writer.writerow(["Land", "Revenue", "Profit", "Best Crop"])
    for i, land in enumerate(LANDS):
        writer.writerow([land, round(result["revenue"][i], 2),
                        round(result["profit"][i], 2),
                        result["best_crops"][i]])
    writer.writerow([])

    writer.writerow(["Statistics (Profit)"])
    writer.writerow(["Mean", "Median", "Std Dev", "Range"])
    writer.writerow([
        round(result["statistics"]["mean"], 2),
        round(result["statistics"]["median"], 2),
        round(result["statistics"]["std"], 2),
        round(result["statistics"]["range"], 2),
    ])
    writer.writerow([])
    writer.writerow(["Best Land", result["best_land"]])
    writer.writerow(["Risk Level", result["risk"]])

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=farming_result.csv"}
    )


@app.route("/set_language/<lang>")
def set_language(lang):
    """Switch the website language. 'en' or 'bn'."""
    if lang in ("en", "bn"):
        session["lang"] = lang
    return redirect(url_for("index"))


# ===== Start the app =====
if __name__ == "__main__":
    init_db()   # create database table on first run
    print("=" * 50)
    print("  Smart Farming Profit Calculator")
    print("  Open browser at: http://127.0.0.1:5000")
    print("=" * 50)
    app.run(debug=True, host="127.0.0.1", port=5000)
