import sqlite3
import pandas as pd
import os

print("=== Accelerated Stage 1: SQL Advanced Aggregation ===\n")

base_dir = os.getcwd()
db_dir = os.path.join(base_dir, 'database')
os.makedirs(db_dir, exist_ok=True)
db_path = os.path.join(db_dir, 'analytics_basic.db')

# １．データベース結線
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS orders")
# 案件データを管理するテーブルを建築（area と budget_man_yen を用意）
cursor.execute('''
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_name TEXT,
    area TEXT,
    budget_man_yen INTEGER
)
''')
cursor.execute("DELETE FROM orders") # データリセット

# テスト用の生データを流し込む
sample_orders = [
    ('Cleint_A', 'Tokyo', 5000),
    ('Cleint_B', 'Tokyo', 3200),
    ('Cleint_C', 'Kanagawa', 4500),
    ('Cleint_D', 'Chiba', 1200),
    ('Cleint_E', 'Tokyo', 8500),
    ('Cleint_F', 'Kanagawa', 2000),
]
cursor.executemany("INSERT INTO orders (client_name, area, budget_man_yen) VALUES (?, ?, ?)", sample_orders)
conn.commit()

# ========================================
# ２．処理：SQLによる「爆速集約(Aggregate)」
# ========================================
# 💡 予測せよ：エリアごとに「グループ化（GROUP BY）し、各エリアの案件数（COUNT）と予算総額（SUM）」を計算する
sql_query = """
SELECT area, COUNT(id) AS total_orders, SUM(budget_man_yen) AS total_budget
FROM orders
GROUP BY area
ORDER BY total_budget DESC
"""

# Pandasのデータフレームへ流し込む
df_aggregated = pd.read_sql_query(sql_query, conn)

print("--- [AGGREGATED OUTPUT] エリア別の自動集計結果 ---")
print(df_aggregated)

# ３．出力
output_dir = os.path.join(base_dir, '成果物')
os.makedirs(output_dir, exist_ok=True)
df_aggregated.to_excel(os.path.join(output_dir, 'area_analytics_report.xlsx'),index=False)

conn.close()
print("\nSYS_STATUS: Aggrefation pipeline executed with Exit Code 0.")