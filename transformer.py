import json
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description="Generate chart data for top domains.")
    parser.add_argument('TERM', type=str, help='The search term to include in file names.')
    return parser.parse_args()

args = parse_arguments()

IN_FILE = f'domain_analysis_{args.TERM}.json'
OUT_FILE = f'chart_data_{args.TERM}.json'

top_n = 5

with open(IN_FILE, 'r', encoding='utf-8') as file:
    domain_counts = json.load(file)

sorted_domains = sorted(domain_counts.items(), key=lambda item: item[1], reverse=True)

top_domains = dict(sorted_domains[:top_n])

others_count = sum(count for _, count in sorted_domains[top_n:])

if others_count > 0:
    top_domains["Others"] = others_count

chart_data = {
    "labels": list(top_domains.keys()),
    "datasets": [
        {
            "label": "Domain Frequency",
            "data": list(top_domains.values()),
            "backgroundColor": [
                "#FF6384", "#36A2EB", "#FFCE56", "#4CAF50"
            ][:len(top_domains)]
        }
    ]
}

with open(OUT_FILE, 'w', encoding='utf-8') as file:
    json.dump(chart_data, file, ensure_ascii=False, indent=4)

print(f"Filtered data saved to '{OUT_FILE}'.")
