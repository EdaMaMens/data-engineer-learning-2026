import requests
from bs4 import BeautifulSoup
import sqlite3
import os
import time

print("=== Accelerated Phase 2: Infinite Crawler & Store ===\n")

# １．ENVIRONMENT SETUP（カレントディレクトリの取得、パスの統合、および既存テーブルの削除）
base_dir = os.getcwd()
db_path = os.path.join(base_dir, 'database', 'infinite_vault.db')

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 初期化処理：既存オブジェクトとの競合を防ぐためテーブルを一度削除
cursor.execute("DROP TABLE IF EXISTS quotes")
cursor.execute('''
CREATE TABLE IF NOT EXISTS quotes(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text_content TEXT,
    author_name TEXT
)
''')
conn.commit()

# ２．AUTOMATED PAGINATION LOOP（while文による無限ループと動的URLの生成）
current_page = 1

while True:
    target_url = f"https://quotes.toscrape.com/page/{current_page}/"
    print(f" -> 🔍 Scanning: {target_url}")

    # HTTP GETリクエストを発行し、レスポンスオブジェクトを取得
    response = requests.get(target_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # HTML構造から特定のクラス属性を持つ要素群を Resultset として一括抽出
    quote_boxes = soup.find_all('div', class_='quote')

    # 各要素（Tagオブジェクト）からデータを抽出し、SQLによるインサートを実行
    for box in quote_boxes:
        text = box.find('span', class_='text').text
        author = box.find('small', class_='author').text

        cursor.execute(
            "INSERT INTO quotes (text_content, author_name) VALUES (?, ?)",
            (text, author)
        )

    #１ページ文のトランザクション処理をデータベースへコミット（永続化）
    conn.commit()

    # ３．PAGINATION TERMINATION CHECK（次のページ要素の有無によるループ脱出判定）
    next_button = soup.find('li', class_='next')

    # 次ページ要素が存在しない（Noneである）場合、最終ページと判定してループを終了
    if not next_button:
        print(" 🏁 [INFO] No more pages found. Exiting loop safely.")
        break

    # カウンター変数をインクリメントし、次回ループのURLを更新
    current_page += 1

    # Webサーバーへの過度集中を回避するための待機処理（１秒スリープ）
    time.sleep(1)

# ４．RESOURCE LIBERATION（データベースコネクションのクローズとロック解除）
conn.close()
print("\n🏆 SYS_STATUS: Complete with Exit Code 0.")