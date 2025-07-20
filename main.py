# /// script
# dependencies = ["playwright", "requests", "pandas", "lxml"]
# ///

from playwright.sync_api import sync_playwright
import pandas as pd
from io import StringIO

def get_html_content(url: str) -> str:
    """Fetch and return the HTML content of a given URL using Playwright."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, channel="chrome")  # You can remove channel="chrome" if not needed
        page = browser.new_page()
        page.goto(url, wait_until="domcontentloaded")
        html = page.content()
        browser.close()
        return html

def html_tables_to_dfs(html: str) -> list:
    """Convert HTML string to a list of pandas DataFrames (one per <table>)."""
    try:
        dfs = pd.read_html(StringIO(html))
        return dfs
    except ValueError:
        return []

def sum_all_table_numbers(dfs: list) -> float:
    """Sum all numeric values in all DataFrames."""
    total = 0
    for df in dfs:
        numeric_df = df.apply(pd.to_numeric, errors='coerce')  # convert all to numeric, ignore non-numeric
        total += numeric_df.sum(numeric_only=True).sum()
    return total

# ✅ Main logic to scrape seed pages and compute total
if _name_ == "_main_":
    total_sum = 0
    for seed in range(6, 16):  # Seed 6 to Seed 15
        url = f"https://sanand0.github.io/tdsdata/js_table/?seed={seed}"
        print(f"Scraping: {url}")
        html = get_html_content(url)
        dfs = html_tables_to_dfs(html)
        seed_total = sum_all_table_numbers(dfs)
        print(f"🔹 Seed {seed} sum: {seed_total}")
        total_sum += seed_total

    print(f"\n TOTAL SUM ACROSS ALL SEEDS: {total_sum}")