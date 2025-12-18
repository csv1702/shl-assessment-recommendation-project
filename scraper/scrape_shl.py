import requests
from bs4 import BeautifulSoup
import json
import time
from urllib.parse import urljoin

# ========================
# CONFIGURATION
# ========================

BASE_URL = "https://www.shl.com"
CATALOG_URL = "https://www.shl.com/products/product-catalog/"
OUTPUT_PATH = "data/raw/assessment_links.json"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; SHLAssessmentBot/1.0)"
}

# Observed valid SHL catalog filters
TYPE_FILTERS = [1, 2, 3, 4, 5, 6, 7]

PAGE_SIZE = 24
MAX_EMPTY_PAGES = 2
REQUEST_DELAY = 1.5

session = requests.Session()
session.headers.update(HEADERS)


# ========================
# HELPERS
# ========================

def fetch_page(url, retries=3):
    for attempt in range(retries):
        try:
            response = session.get(url, timeout=30)
            response.raise_for_status()
            return BeautifulSoup(response.text, "html.parser")
        except requests.exceptions.RequestException:
            time.sleep(2)
    return None


def is_valid_assessment_link(href: str) -> bool:
    """
    Valid Individual Test Solution URLs:
    /products/product-catalog/view/<assessment-slug>/
    """
    return (
        href.startswith("/products/product-catalog/view/")
        and "?" not in href
    )


# ========================
# MAIN CRAWLER
# ========================

def scrape_assessment_links():
    collected_links = set()

    for type_id in TYPE_FILTERS:
        print(f"\n=== Scraping catalog TYPE={type_id} ===")

        start = 0
        empty_pages = 0

        while True:
            url = f"{CATALOG_URL}?type={type_id}&start={start}"
            print(f"Fetching: {url}")

            soup = fetch_page(url)
            if soup is None:
                print("⚠️ Page skipped due to repeated failures.")
                start += PAGE_SIZE
                continue

            new_links = 0

            for a in soup.find_all("a", href=True):
                href = a["href"]

                if is_valid_assessment_link(href):
                    full_url = urljoin(BASE_URL, href)
                    if full_url not in collected_links:
                        collected_links.add(full_url)
                        new_links += 1

            print(f"New assessments found: {new_links}")
            print(f"Total collected so far: {len(collected_links)}")

            if new_links == 0:
                empty_pages += 1
                if empty_pages >= MAX_EMPTY_PAGES:
                    print("No more assessments for this type.")
                    break
            else:
                empty_pages = 0

            start += PAGE_SIZE
            time.sleep(REQUEST_DELAY)

    # Save results
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(sorted(collected_links), f, indent=2)

    print("\n✅ STEP 4.3 COMPLETED SUCCESSFULLY")
    print(f"Total Individual Test Solutions collected: {len(collected_links)}")


if __name__ == "__main__":
    scrape_assessment_links()
