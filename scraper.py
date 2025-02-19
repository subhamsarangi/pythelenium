import json
import argparse
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time

SEARCH_ENGINE = 'https://duckduckgo.com'
def parse_arguments():
    parser = argparse.ArgumentParser(description=f"Scrape search results from {SEARCH_ENGINE}.")
    parser.add_argument('TERM', type=str, help=f'The search query for {SEARCH_ENGINE}.')
    parser.add_argument('--pages', type=int, default=3, help='Number of pages to scrape.')
    return parser.parse_args()

args = parse_arguments()
TERM = args.TERM

opts = Options()
opts.add_argument('--headless')  
opts.add_argument('--disable-gpu')

browser = Chrome(options=opts)

browser.get(SEARCH_ENGINE)
search_box = browser.find_element(By.ID, 'searchbox_input')
search_box.send_keys(TERM)
search_box.submit()

browser.implicitly_wait(3)

scraped_data = []
OUT_FILE = f'scraped_data_{TERM}.json'


for page in range(args.pages):  
    results = browser.find_elements(By.CSS_SELECTOR, 'a[data-testid="result-title-a"]')
    for result in results:
        title = result.find_element(By.TAG_NAME, 'span').text
        url = result.get_attribute('href')
        scraped_data.append({"title": title, "url": url})

    try:
        more_button = browser.find_element(By.ID, 'more-results')
        ActionChains(browser).move_to_element(more_button).click().perform()
        time.sleep(2)
    except Exception as e:
        print(f"Error clicking 'More results' button: {e}")
        break

with open(OUT_FILE, 'w', encoding='utf-8') as file:
    json.dump(scraped_data, file, ensure_ascii=False, indent=4)

browser.quit()

print(f"Scraping complete. Data saved to {OUT_FILE}.")
