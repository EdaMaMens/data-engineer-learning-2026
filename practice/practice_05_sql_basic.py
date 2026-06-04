import sqlite3
import pandas as pd
import os
from datetime import datetime

print("=== Week 1 Day 3: Python * SQL Database Pipeline (Fixed) ===\n")

# ====================================================
# 0. DIRECTORY SETUP (環境に依存しない絶対パスの確実な建築)
# ====================================================
# 現在実行している作業フォルダ（カレントディレクトリ）の正確な絶対住所を取得
base_dir = os.getcwd()

# 確実に「data-engineer-learning-2026」の直下、または現在の作業スペース内に『database』の動線を引く
db_dir = os.path.join(base_dir, 'database')

# 【安全装置】フォルダが存在しなければ、最優先で確実に物理建築する
if not os.path.exists(db_dir):
    os.makedirs(db_dir, exist_ok=True) # exist_ok=True で衝突バグを完全防止
    print(f"DIR_STATUS: Created database directory at {db_dir}")

db_path = os.path.join(db_dir, 'market_data.db')
print(f"DB_PATH_TARGET: {db_path}")

# ====================================================
# 1. DATABASE BUILD * INSERT (テーブル建築 ＆ データ流し込み)
# ====================================================
# 確保した確実な住所（db_path）を使ってパイプを結線
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_name TEXT,
    area TEXT,
    budget_man_yen INTEGER,
    status TEXT
)
''')

cursor.execute("DELETE FROM projects")

sample_data = [
    ('A_New_Construction', 'Tokyo', 4500, 'In_Progress'),
    ('B_Renovation', 'Kanagawa', 2800, 'In_Progress'),
    ('C_Large_Repair', 'Chiba', 12500, 'Completed'),
    ('D_After_Support', 'Tokyo', 320, 'After_Service'),
    ('E_Wall_Construction', 'Tokyo', 3250, 'In_Progress')
]

cursor.executemany(
    "INSERT INTO projects (project_name, area, budget_man_yen, status) VALUES (?, ?, ?, ?)",
    sample_data
)
conn.commit()
print("DB_STATUS: Database and 'projects' table built successfully.")

# ====================================================
# 2. SQL QUERY * PANDAS EXTRACT (SQL抽出 ＆ Pandas変換)
# ====================================================
sql_query = """
SELECT project_name, budget_man_yen, status 
FROM projects 
WHERE area = 'Tokyo' AND budget_man_yen >= 3000
ORDER BY budget_man_yen DESC
"""

df_filtered = pd.read_sql_query(sql_query, conn)

print("\n--- [OUTPUT] SQL Filtered Result (Tokyo / Budget >= 30,000,000 Yen) ---")
print(df_filtered)

# ====================================================
# 3. EXPORT * CLOSE (成果物保存 ＆ パイプ切断)
# ====================================================
# 出力先フォルダも同様に確実に固定
output_dir = os.path.join(base_dir, '成果物')
if not os.path.exists(output_dir):
    os.makedirs(output_dir, exist_ok=True)

output_path = os.path.join(output_dir, 'tokyo_large_projects_report.xlsx')
df_filtered.to_excel(output_path, index=False)

conn.close()

print(f"\nSYS_STATUS: Export completed successfully.")
print(f"PATH: {output_path}")
print(f"TIME: {datetime.now()}")