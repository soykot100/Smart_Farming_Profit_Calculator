#!/usr/bin/env python
"""
take_screenshots.py
-------------------
Starts the Flask app, opens it in a headless browser, fills the form,
and saves screenshots for use in the presentation.
"""
import subprocess
import time
import os
from playwright.sync_api import sync_playwright

OUT_DIR = "/home/z/my-project/download/slides/img"
os.makedirs(OUT_DIR, exist_ok=True)
APP_DIR = "/home/z/my-project/download/smart-farming-flask"

def start_flask():
    proc = subprocess.Popen(
        ["python", "-c", "from app import app, init_db; init_db(); app.run(debug=False, use_reloader=False, host='127.0.0.1', port=5000)"],
        cwd=APP_DIR,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    time.sleep(4)
    return proc

def stop_flask(proc):
    proc.terminate()
    try:
        proc.wait(timeout=5)
    except:
        proc.kill()

def main():
    print("Starting Flask app...")
    flask_proc = start_flask()
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={"width": 1400, "height": 900})

            # Screenshot 1: Home page (empty form)
            print("Screenshot 1: Home page")
            page.goto("http://127.0.0.1:5000/", wait_until="networkidle")
            page.wait_for_timeout(800)
            page.screenshot(path=os.path.join(OUT_DIR, "shot1_home.png"))

            # Screenshot 2: Form filled
            print("Screenshot 2: Form filled")
            yields = [[1000, 800, 500], [900, 700, 600], [1100, 850, 550]]
            for i in range(3):
                for j in range(3):
                    page.fill(f"input[name='yield_{i}_{j}']", str(yields[i][j]))
            for j, p_val in enumerate([25, 30, 20]):
                page.fill(f"input[name='price_{j}']", str(p_val))
            for i, c in enumerate([15000, 12000, 18000]):
                page.fill(f"input[name='cost_{i}']", str(c))
            page.click("label.weather-opt:has(input[value='good']) .weather-card")
            page.wait_for_timeout(500)
            page.screenshot(path=os.path.join(OUT_DIR, "shot2_form_filled.png"))

            # Submit form
            page.click("button[type='submit']")
            page.wait_for_timeout(2000)

            # Screenshot 3: Results top (KPI + charts)
            print("Screenshot 3: Results top")
            page.screenshot(path=os.path.join(OUT_DIR, "shot3_results_top.png"))

            # Screenshot 4: Charts section
            print("Screenshot 4: Charts")
            page.evaluate("window.scrollBy(0, 500)")
            page.wait_for_timeout(1000)
            page.screenshot(path=os.path.join(OUT_DIR, "shot4_charts.png"))

            # Screenshot 5: Table + statistics
            print("Screenshot 5: Stats + table")
            page.evaluate("window.scrollBy(0, 400)")
            page.wait_for_timeout(500)
            page.screenshot(path=os.path.join(OUT_DIR, "shot5_stats.png"))

            # Screenshot 6: T-Test
            print("Screenshot 6: T-Test")
            page.evaluate("window.scrollBy(0, 400)")
            page.wait_for_timeout(1000)
            page.screenshot(path=os.path.join(OUT_DIR, "shot6_ttest.png"))

            # Screenshot 7: Bangla language
            print("Screenshot 7: Bangla")
            page.evaluate("window.scrollTo(0, 0)")
            page.click("a[href*='set_language/bn']")
            page.wait_for_timeout(1500)
            page.screenshot(path=os.path.join(OUT_DIR, "shot7_bangla.png"))

            # Switch back to English
            page.click("a[href*='set_language/en']")
            page.wait_for_timeout(800)

            # Save the result and go to history
            print("Screenshot 8: History page")
            # Click Save button by its form action
            page.evaluate("""() => {
                const forms = document.querySelectorAll('form[action*="/save"]');
                if (forms.length > 0) forms[0].submit();
            }""")
            page.wait_for_timeout(2000)
            page.screenshot(path=os.path.join(OUT_DIR, "shot8_history.png"))

            browser.close()
            print("All screenshots saved to:", OUT_DIR)
            for f in sorted(os.listdir(OUT_DIR)):
                print(" -", f)
    finally:
        stop_flask(flask_proc)

if __name__ == "__main__":
    main()
