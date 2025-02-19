import json
import argparse
from urllib.parse import urlparse
from collections import Counter

def parse_arguments():
    parser = argparse.ArgumentParser(description="Analyze scraped data and count domains.")
    parser.add_argument('TERM', type=str, help='The search term to include in file names.')
    return parser.parse_args()

args = parse_arguments()

IN_FILE = f'scraped_data_{args.TERM}.json'
OUT_FILE = f'domain_analysis_{args.TERM}.json'

with open(IN_FILE, 'r', encoding='utf-8') as file:
    scraped_data = json.load(file)

domains = [urlparse(entry["url"]).netloc for entry in scraped_data]

domain_counts = Counter(domains)

sorted_domain_counts = dict(sorted(domain_counts.items(), key=lambda item: item[1], reverse=True))

with open(OUT_FILE, 'w', encoding='utf-8') as file:
    json.dump(sorted_domain_counts, file, ensure_ascii=False, indent=4)

print(f"Domain analysis complete. Data saved to '{OUT_FILE}'.")
