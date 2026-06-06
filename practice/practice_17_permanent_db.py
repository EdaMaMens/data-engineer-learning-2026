import os
import sqlite3

# PC内の「現在のフォルダー」の絶対パスを自動取得
current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_dir, "choslit_BIM.db")

print(f"DATABASE FILE PATH -> {db_path}")

# メモリではなく、指定した住所に本物の「choslit_BIM.db」ファイルを生成して接続
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 永久保存される、データ保管用の「inventoryテーブル」を建築
cursor.execute("""
    CREATE TABLE IF NOT EXISTS inventory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_name TEXT,
    status text
    )
""")

# 実践データをテスト挿入
cursor.execute(
    "INSERT INTO inventory (item_name, status) VALUES (?, ?)",
    ("Rode NTG4+", "仕入れ完了")
)
conn.commit()

# ファイルに本当に保存されたかをSERCT文で監査確認
cursor.execute("SElECT * FROM inventory")
row = cursor.fetchone()
print(f"STORED_DATA -> ID: {row[0]} | NAME: {row[1]} | STATUS: {row[2]}")

# 安全に閉じる
conn.close()
print("\nALL PROCESS FINISHED WITH EXIT CODE 0")