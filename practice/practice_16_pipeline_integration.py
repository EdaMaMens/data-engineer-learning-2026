import sqlite3
from bs4 import BeautifulSoup

# 何度実行してもPCを汚さない、使い捨てのメモリ内DB領域を確保
conn = sqlite3.connect(":memory:")
cursor = conn.cursor()

# 仕切り（型）を厳格に指定した、データ格納用「itemsテーブル」を建築
cursor.execute("""
    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        weight INTEGER
    )
""")
conn.commit()

# 実証用の模擬HTMLデータセット（15の3パターンを継承）
mock_html_list = [
    '<div class="item">品名: マイク <span class="weight">176g</span></div>',
    '<div class="item">品名: 不明スピーカー <span class="weight"></span></div>',
    '<div class="item">品名: モニターアーム </div>'
]

print("--- START PIPELINE INTEGRATION ---")

for html in mock_html_list:
    soup = BeautifulSoup(html, "html.parser")

    # HTMLの文字列を「品名:」で分解し、純粋な名前だけを抽出
    item_text = soup.find(class_="item").text
    item_name = item_text.split("品名: ")[1].split("<")[0].strip()

    weight_element = soup.find(class_="weight")

    # 重量の欠損（Noneや空文字）を検出し、安全な数値「0」に整形
    if weight_element is None:

        cleaned_weight = 0
    else:
        # タグが存在するなら、この段階で【最初に1回だけ】文字を抜き、空白を削って変数に入れる！
        raw_weight_text = weight_element.text.strip()

        if raw_weight_text == "":
            # タグの中身が空っぽ（パターン2）なら0g
            cleaned_weight = 0
        else:
            # 文字（"176g"）が確実に入っている（パターン1）ので、安全に"g"を削って数値化できる！
            cleaned_weight = int(raw_weight_text.replace("g", ""))

    # SQLインジェクション攻撃を防ぐため、？（バインド変数）を介して安全に挿入
    cursor.execute(
        "INSERT INTO items (name, weight) VALUES (?, ?)",
        (item_name, cleaned_weight)
    )

conn.commit()
print("DATABASE INSERT SUCCESSFUL.")

# データベースに正しく格納されたかを全件抽出してコンソール確認
print("\n--- FINAL DATABASE INSPECTION ---")
cursor.execute("SELECT id, name, weight FROM items")
rows = cursor.fetchall()

for row in rows:
    print(f"DB_ROW -> ID: {row[0]} NAME: {row[1]} | WEIGHT: {row[2]}g")

# メモリリークを防ぐため、使い終わったコネクションを安全に切断
conn.close()
print("\nALL PROCESS FINISHED WITH EXIT CODE 0")