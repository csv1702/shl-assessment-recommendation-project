import json
import time
import requests
from bs4 import BeautifulSoup
from pathlib import Path

# ========================
# CONFIG
# ========================

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; SHLAssessmentBot/1.0)"
}

INPUT_PATH = Path("data/raw/assessment_links.json")
OUTPUT_PATH = Path("data/processed/shl_catalogue.json")

REQUEST_DELAY = 1.2
TIMEOUT = 30
RETRIES = 3

session = requests.Session()
session.headers.update(HEADERS)


# ========================
# HELPERS
# ========================

def fetch_page(url):
    for _ in range(RETRIES):
        try:
            response = session.get(url, timeout=TIMEOUT)
            response.raise_for_status()
            return BeautifulSoup(response.text, "html.parser")
        except requests.exceptions.RequestException:
            time.sleep(2)
    return None


def safe_text(soup, selector):
    el = soup.select_one(selector)
    return el.get_text(strip=True) if el else "Not specified"


def extract_list_after_label(soup, label_text):
    """
    Extract comma-separated values that appear after a label.
    """
    text = soup.get_text(" ").lower()
    label = label_text.lower()
    if label not in text:
        return "Not specified"

    parts = text.split(label, 1)[1]
    return parts.split(".")[0].strip()


# ========================
# DETAIL SCRAPER
# ========================

def scrape_assessment_details(url):
    soup = fetch_page(url)
    if soup is None:
        return None

    name = safe_text(soup, "h1")
    description = safe_text(soup, "div.product-description")

    full_text = soup.get_text(" ").lower()

    # Duration
    duration = "Not specified"
    for token in full_text.split():
        if token.isdigit():
            duration = token
            break

    # Job levels & languages (best-effort)
    job_levels = extract_list_after_label(soup, "job level")
    languages = extract_list_after_label(soup, "language")

    remote_support = "Yes" if "remote" in full_text else "No"
    adaptive_support = "Yes" if "adaptive" in full_text else "No"

    return {
        "name": name,
        "url": url,
        "description": description,
        "duration": duration,
        "job_levels": job_levels,
        "languages": languages,
        "remote_support": remote_support,
        "adaptive_support": adaptive_support
    }


# ========================
# MAIN PIPELINE
# ========================

def run_detail_scraping():
    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        urls = json.load(f)

    results = []
    total = len(urls)

    print(f"Scraping details for {total} assessments\n")

    for idx, url in enumerate(urls, start=1):
        print(f"[{idx}/{total}] {url}")

        data = scrape_assessment_details(url)
        if data:
            results.append(data)

        time.sleep(REQUEST_DELAY)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print(f"Total assessments saved: {len(results)}")
    print(f"Output file: {OUTPUT_PATH}")


if __name__ == "__main__":
    run_detail_scraping()
