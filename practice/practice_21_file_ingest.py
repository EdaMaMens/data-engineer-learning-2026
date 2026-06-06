import os
import sqlite3

# 現在のスクリプトの配置ディレクトリから各ファイルの絶対パスを生成
current_dir = os.path.dirname(os.path.abspath(__file__))
txt_path = os.path.normpath(os.path.join(current_dir, "raw_inventory.txt"))
db_path = os.path.normpath(os.path.join(current_dir, "choslit_BTM_ingest.db"))

# テスト用の外部テキストファイルを自動生成
with open(txt_path, "w", encoding="utf-8") as f:
    f.write("Sony ZV-E10\n ,仕入れ完了\n")
    f.write(" Zoom M4   ,仕入れ完了\n")
    f.write("Sony ZV-E10\n ,仕入れ完了\n")
    f.write("Rode NTG4+\n ,仕入れ完了\n")

# １．データベース接続とテーブル作成
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

print("--- START FILE INGEST PIPLINE ---")

# テキストファイルの読み込みとデータクレンジング
with open(txt_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

for line in lines:
    parts = line.split(",")
    if len(parts) == 2:
        clean_name = parts[0].replace("\n", "").strip()
        clean_status = parts[1].replace("\n", "").strip()
        # クレンジング済データをテーブルへインサート（重複時、IGNOREでスキップ）
        cursor.execute(
            "INSERT OR IGNORE INTO inventory (item_name, status) VALUES (?, ?)",
            (clean_name, clean_status)
        )

conn.commit()
print("FILE INGEST AND BULK INSERT SUCCESSFUL.")

# ３．テーブルの格納データをSELECT文で抽出して確認
print("\n--- FINAL DATABASE INSPECTION ---")
cursor.execute("SELECT id, item_name, status FROM inventory")
rows = cursor.fetchall()

for row in rows:
    print(f"DB_ROW -> ID: {row[0]} | NAME: '{row[1]}' | STATUS: {row[2]}")

conn.close()
print("\nALL PROCESS FINISHED WITH EXIT CODE 0")