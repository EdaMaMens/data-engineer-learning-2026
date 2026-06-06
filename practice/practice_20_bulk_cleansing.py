import os
import sqlite3

# 現在のスクリプトの配置ディレクトリから、データベースファイルの絶対パスを生成
current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.normpath(os.path.join(current_dir, "choslit_BTM_bulk.db"))

# 1. SQLiteデータベースへの接続とテーブル作成（item_nameにUNIQUE制約を設定）
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

# ２．テスト用の入力データ
raw_data_list = [
    {"name": "Sony ZV-E10\n ", "status": "仕入れ完了"},
    {"name": " Zoom M4  ", "status": "仕入れ完了"},
    {"name": "Sony ZV-E10\n ", "status": "仕入れ完了"},  # 重複データ
    {"name": "Rode NTG4+\n", "status": "仕入れ完了"},
]

print("---START BULK DATA CLEANSING PIPLINE ---")

# ３．ループ処理によるデータのクレンジングとデータベースへのインサート
for data in raw_data_list:
    clean_name = data["name"].replace("\n", "").strip()

    # INSERT OR IGNORE を利用しUNIQUE制約による重複エラー発生は処理をスキップ
    cursor.execute(
        "INSERT OR IGNORE INTO inventory (item_name, status) VALUES (?, ?)",
        (clean_name, data["status"])

    )

conn.commit()
print("BULK INSERT AND CLEANING SUCCESSFUL.")

# ４．インサート後の格納データをSELECT文で抽出して確認
print("\n--- FINAL DATABASE INSPECTION ---")
cursor.execute("SELECT id, item_name, status FROM inventory")
rows = cursor.fetchall()

for row in rows:
    print(f"DB_ROW -> ID: {row[0]} | NAME: '{row[1]}' | STATUS: {row[2]}")

conn.close()
print("\nALL PROCESS FINISHED WITH EXIT CODE 0")