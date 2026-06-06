import os
import sqlite3

# 現在のフォルダの絶対住所から、DBファイルのパスを確定（17の配管を継承）
current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_dir, "shoslit_BIM_safr.db")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# item_nameの直後に「UNIQUE」を付与し、重複を絶対に許さない仕切り
cursor.execute("""
    CREATE TABLE IF NOT EXISTS inventory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_name TEXT UNIQUE,
        status TEXT
        )
""")
conn.commit()

# 普通のINSERTではなく「OR IGNORE」を添えて、ダブり時は自動スルーする
cursor.execute(
    "INSERT OR IGNORE INTO inventory (item_name, status) VALUES (?, ?)",
    ("Rode NTG4+", "仕入れ完了")
)
conn.commit()

# データベースの全件を引っ張り出して監査確認
print("---FINAL DATABASE INSPECTION ---")
cursor.execute("SELECT * FROM inventory")
rows = cursor.fetchall()

for row in rows:
    print(f"DB_ROW -> ID: {row[0]} | NAME: {row[1]} | STATUS: {row[2]}")

conn.close()
print("\nALL PROCESS FINISHED WITH EXIT CODE 0")