import subprocess
import os
import time

TERM = "LORA PEFT"

file_map = {
    'scraper.py': {
        'input': None,
        'output': f'scraped_data_{TERM}.json'
    },
    'analyser.py': {
        'input': f'scraped_data_{TERM}.json',
        'output': f'domain_analysis_{TERM}.json'
    },
    'transformer.py': {
        'input': f'domain_analysis_{TERM}.json',
        'output': f'chart_data_{TERM}.json'
    }
}

def run_script(script_name, *args):
    subprocess.run(['poetry', 'run', 'python', script_name] + list(args), check=True)

def wait_for_file(file_path):
    while not os.path.exists(file_path):
        time.sleep(2)

def generate_html():
    with open('template_chart.html', 'r', encoding='utf-8') as template_file:
        html_content = template_file.read()

    html_content = html_content.replace("{TERM}", TERM)
    
    with open(f'index_{TERM}.html', 'w', encoding='utf-8') as file:
        file.write(html_content)

def automate_process():
    for script, files in file_map.items():
        if files['input']:
            wait_for_file(files['input'])
        run_script(script, TERM)
        wait_for_file(files['output'])

    generate_html()

if __name__ == "__main__":
    automate_process()
