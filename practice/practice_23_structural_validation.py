import os
import sqlite3

# スクリプトの配置ディレクトリから、各ファイルの絶対パスを生成
current_dir = os.path.dirname(os.path.abspath(__file__))
txt_path = os.path.normpath(os.path.join(current_dir, "raw_inventory_v3.txt"))
db_path = os.path.normpath(os.path.join(current_dir, "choslit_BIM_structural.db"))

# --- 検証用テキストファイルの自動生成 ---
with open(txt_path, "w", encoding="utf-8") as f:
    f.write("Sony ZV-E10,仕入れ完了\n")
    f.write("Zoom M4_no_comma_error\n")  # 構造破壊データ（カンマなし）
    f.write(" ,仕入れ完了\n")  # 不純物データ（ちぎれ空文字）
    f.write("Rode NTG4+,仕入れ完了\n")

# 1. データベース接続とテーブル作成
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

print("--- START STRUCTURAL VALIDATION PIPELINE ---")

# 2. テキストファイルの読み込みと多層データ検閲
with open(txt_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

for line in lines:
    clean_line = line.replace("\n", "").strip()

    # 🛠️ [開発必須]: 第0防壁（カンマの存在チェック）
    # 💡 [学習解説]: 文字列内にカンマ（","）が1つも含まれていない行は、分割処理に進めず即座に破棄する
    if "," not in clean_line:
        print(f"[CRITICAL WARNING] カンマ未検出（構造破壊）のためスキップ: '{clean_line}'")
        continue

    # 第0防壁を通過した（必ずカンマが存在する）データのみ分割を許可
    parts = clean_line.split(",")

    # 🛠️ [開発必須]: 第1防壁（部屋数の厳密監査）
    if len(parts) != 2:
        print(f"[CRITICAL WARNING] 分割数異常のためスキップ: '{clean_line}'")
        continue

    # 構造の安全性が100%確定したため、安全に変数を展開（IndexErrorは絶対に起きない）
    clean_name = parts[0].strip()
    clean_status = parts[1].strip()

    # 🛠️ [開発必須]: 第2防壁（中身の空文字チェック）
    if not clean_name:
        print(f"[WARNING] 商品名欠損のためスキップ: STATUS={clean_status}")
        continue

    # すべての検閲をクリアした正常データのみ、データベースへインサート
    cursor.execute(
        "INSERT OR IGNORE INTO inventory (item_name, status) VALUES (?, ?)",
        (clean_name, clean_status)
    )

conn.commit()
print("BULK INSERT SUCCESSFUL.")

# 3. テーブルの格納データをSELECT文で抽出して確認
print("\n--- FINAL DATABASE INSPECTION ---")
cursor.execute("SELECT id, item_name, status FROM inventory")
rows = cursor.fetchall()

for row in rows:
    print(f"DB_ROW -> ID: {row[0]} | NAME: '{row[1]}' | STATUS: {row[2]}")

conn.close()
print("\nALL PROCESS FINISHED WITH EXIT CODE 0")