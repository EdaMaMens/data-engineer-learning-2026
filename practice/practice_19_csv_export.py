import csv
import os
import  sqlite3

# 現在のフォルダの絶対住所から読み込みDBと書き出すCSVの住所を確定
current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_dir, "choslit_BTM_safe.db")
csv_path = os.path.join(current_dir, "exported_items.csv")

# １．データベースからデータを抽出（仕入れ）
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS inventory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_name TEXT UNIQUE,
        status TEXT
    )
""")
conn.commit()

# 実戦テストデータが完全に空だった場合のために、1件安全にモックを挿入しておく
cursor.execute("INSERT OR IGNORE INTO inventory (item_name, status) VALUES (?, ?)", ("Rode NTG4+", "仕入れ完了"))
conn.commit()

cursor.execute("SELECT id, item_name, status FROM inventory")
rows = cursor.fetchall()  # DBの中身を丸ごと rows に一括取得
conn.close()

print(f"EXTRACTED {len(rows)} ROWS FROM DATABASE.")

# ２．外部のCSVファイルへの書き出し（搬出インフラ）
with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
    write = csv.writer(f)
    write.writerow(["ID", "商品名", "ステータス"])  # 一番上の見出し（ヘッダー行）を書き込む
    write.writerow(rows)  # データベースから抜いた行データを一括でCSVへ流し込む

print(f"CSV EXPORT SUCCESSFUL -> {csv_path}")
print("\nALL PROCESS FINISHED WITH EXIT CODE 0 ")