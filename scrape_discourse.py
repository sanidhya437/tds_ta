import json
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import threading

# --- Config ---
TDS_KB_URL = "https://discourse.onlinedegree.iitm.ac.in/c/courses/tds-kb/34"
START_DATE = datetime(2025, 5, 1)
END_DATE = datetime(2025, 6, 30)
OUTPUT_JSON = "tds_kb_posts.json"

# --- Setup Driver ---
options = Options()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

print("[INFO] Open the browser, login manually, and then press Enter to continue...")
driver.get(TDS_KB_URL)
input("[USER ACTION] After logging in manually, press Enter to continue scraping...")

# --- Scroll to Load All Posts ---
last_height = driver.execute_script("return document.body.scrollHeight")
print("[INFO] Scrolling to load posts. Press Enter in this console to stop.")

stop_scrolling = False

def wait_for_enter():
    global stop_scrolling
    input("[🖱️  USER ACTION] Press Enter to stop scrolling...\n")
    stop_scrolling = True

# Start a background thread to wait for Enter key
threading.Thread(target=wait_for_enter, daemon=True).start()

while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if stop_scrolling or new_height == last_height:
        print("[INFO] 🛑 Stopped scrolling.")
        break
    last_height = new_height

# --- Parse Posts ---
soup = BeautifulSoup(driver.page_source, "html.parser")
driver.quit()

print("[INFO] 🧵 Parsing visible posts...")
base_url = "https://discourse.onlinedegree.iitm.ac.in"
results = []

for row in soup.select("tr.topic-list-item"):
    title_tag = row.select_one("a.title")
    link = base_url + title_tag['href'] if title_tag else None
    title = title_tag.get_text(strip=True) if title_tag else "(No title)"

    activity_td = row.select_one("td[class*='activity']")
    if activity_td and 'title' in activity_td.attrs:
        created_str = activity_td['title'].split("\n")[0].replace("Created: ", "").strip()
        try:
            created_date = datetime.strptime(created_str, "%b %d, %Y %I:%M %p")
        except Exception as e:
            print(f"[WARN] Could not parse date: {created_str}")
            continue
        if START_DATE <= created_date <= END_DATE:
            results.append({
                "title": title,
                "link": link,
                "content": "(Content will require page-level scraping if needed)"
            })

# --- Save to JSON ---
with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=4, ensure_ascii=False)

print(f"[✅] Extracted {len(results)} posts saved to {OUTPUT_JSON}")
