import requests
from bs4 import BeautifulSoup
import sqlite3
import os
import time

print("=== Accelerated Phase 2: File 1 [CRAWLER & STORE] ===\n")

# １．ENVIRONMENT SETUP （絶対住所の建築と環境依存の排除）
base_dir = os.getcwd()
db_dir = os.path.join(base_dir, 'database')
os.makedirs(db_dir, exist_ok=True)
db_path = os.path.join(db_dir, 'multi_page_vault.db')

# ２．DATABASE COUNNECT & INITIALIZE（パイプラインの開通の棚の建築）
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS quotes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text_content TEXT,
    author_name TEXT
)
''')
cursor.execute("DELETE FROM quotes")
conn.commit()

# ３．MULTI-PAGE CRAWLER LOOP（3ページ目の自動巡回 ＆ データベース直撃流し込み）
for page_num in range(1, 4):
    target_url = f"https://quotes.toscrape.com/page/{page_num}"
    print(f" ->🔍 Fetching Data from: {target_url}")
    response = requests.get(target_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    quote_boxes = soup.find_all('div', class_='quote')
    for box in quote_boxes:
        text = box.find('span', class_='text').text
        author = box.find('small', class_='author').text
        cursor.execute(
            "INSERT INTO quotes (text_content, author_name) VALUES (?, ?)",
            (text, author)
        )
    conn.commit()
    time.sleep(1)

conn.close()
print("\n🏆 SYS_STATUS; File 1 [CRAWLER & STORE] completed with Exit Code 0.")