import requests
from bs4 import BeautifulSoup
import os
import pandas as pd
from datetime import datetime

print("=== Week 1 Day 3: Web Scraping Pipeline (Final Fix) ===\n")

# ====================================================
# 1. INPUT
# ====================================================
# ここで完全に「target_url」という箱を定義（結線）
target_url = "https://example.com"

# 定義した直後の箱をそのまま requests.get に流し込む
response = requests.get(target_url)

# ====================================================
# 2. PROCESS
# ====================================================
soup = BeautifulSoup(response.text, 'html.parser')

page_title = soup.find('h1').text
print(f"📡 [SUCCESS] Extracted Title: {page_title}")

page_text = soup.find('p').text
print(f"📡 [SUCCESS] Extracted Content: {page_text}")

# ====================================================
# 3. OUTPUT
# ====================================================
extracted_data = {
    'get_time': [datetime.now()],
    'source_url': [target_url],
    'title': [page_title],
    'content': [page_text]
}

df_web = pd.DataFrame(extracted_data)

base_dir = os.getcwd()
output_dir = os.path.join(base_dir, '成果物')
if not os.path.exists(output_dir):
    os.makedirs(output_dir, exist_ok=True)

output_path = os.path.join(output_dir, 'web_extracted_report.xlsx')
df_web.to_excel(output_path, index=False)

print(f"\n%s" % "SYS_STATUS: Web data successfully pipe-lined to Excel.")
print(f"PATH: {output_path}")