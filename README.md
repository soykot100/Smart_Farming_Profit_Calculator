# Smart Farming Profit Calculator

A simple Flask web app for our Simulation Lab project. Built with Python and Flask — easy to run in VS Code and easy to explain to mam.

## Features

### Lab Tasks (what mam taught)
1. **Matrix Multiplication** — 3x3 yield matrix × 3x1 price vector = revenue per land
2. **Statistics** — Mean, Median, Std Dev, Range
3. **Visualization** — Heatmap of yield matrix + Bar chart of profit
4. **T-Test (A/B Testing)** — Test if a new organic fertilizer increases yield

### Innovative Features
5. **Weather Simulation** — Normal / Good Rain (+20%) / Drought (-30%) / Flood (-50%)
6. **Risk Level** — Low / Medium / High based on standard deviation
7. **Cost & Profit** — Subtract seed + fertilizer + labor cost from revenue

### Smart Features
8. **Crop Recommendation** — Suggests the best crop for each land
9. **Save History** — Save calculations to SQLite, view them later
10. **Export CSV** — Download the result as a CSV file
11. **Bilingual** — Toggle between English and Bangla (EN / বাং button)

## How to Run in VS Code

### Step 1 - Open the folder in VS Code
File → Open Folder → select `smart-farming-flask`

### Step 2 - Install dependencies
Open Terminal (Ctrl + `) and run:
```
pip install -r requirements.txt
```

If you get any error about numpy/scipy, try:
```
pip install --no-cache-dir -r requirements.txt
```

### Step 3 - Run the app
```
python app.py
```

### Step 4 - Open in browser
Go to: http://127.0.0.1:5000

### Step 5 - Stop the app
Press Ctrl + C in the terminal.

## File Structure (simple - easy to understand)

```
smart-farming-flask/
├── app.py              <-- Main Flask app (all logic in one file)
├── translations.py     <-- English + Bangla text dictionary
├── requirements.txt    <-- List of packages to install
├── README.md           <-- This file
├── farming.db          <-- SQLite database (auto-created on first run)
├── templates/
│   ├── index.html      <-- Main calculator page
│   └── history.html    <-- Saved calculations page
└── static/
    └── css/
        └── style.css   <-- Fresh Green theme styles
```

## How to Use the App

1. Enter yield (kg) for each land and crop in Step 1.
2. Enter price per kg for each crop in Step 2.
3. Enter total cost for each land in Step 3.
4. Pick a weather condition in Step 4.
5. Click **Calculate**.
6. See results - KPI cards, charts, table, statistics, T-Test.
7. Click **Save Result** to store in history.
8. Click **Export CSV** to download a CSV file.
9. Use **EN / বাং** button (top right) to switch language.

## How to Explain to Mam (quick guide)

When mam asks about any part, point to the matching function in `app.py`:

| Mam asks about         | Show this function in app.py          |
|------------------------|----------------------------------------|
| Matrix multiplication  | `calculate_revenue()`                  |
| Statistics             | `calculate_statistics()`               |
| T-Test                 | `run_t_test()`                          |
| Weather simulation     | `apply_weather()`                       |
| Risk level             | `get_risk_level()`                      |
| Cost & profit          | `calculate_profit()`                    |
| Best crop              | `find_best_crop_per_land()`             |
| Database               | `init_db()`, `save_to_db()`             |

Each function has a comment explaining what it does. Read the comment aloud.

## Built With

- Python 3
- Flask (web framework)
- NumPy (matrix math + statistics)
- SciPy (T-Test)
- SQLite (database, built into Python)
- Chart.js (charts)
- HTML, CSS, JavaScript

## Author
Simulation Project - Smart Farming Profit Calculator
