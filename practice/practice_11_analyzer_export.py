import sqlite3
import pandas as pd
import os

print("=== Accelerated Phase 2: File 2 [ANALYZER & EXPORT] ===\n")

# １．ENVIRONMENT SETUP（絶対パスの固定と出力先フォルダの自動建築）
base_dir = os.getcwd()
db_path = os.path.join(base_dir, 'database', 'multi_page_vault.db')
output_dir = os.path.join(base_dir, '成果物')
os.makedirs(output_dir, exist_ok=True)

# ２．DATABASE CONNECT（倉庫のパイプ開通と職人の配置）
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# ３．SQL EXTRACT（倉庫内の大量データから、必要なものだけを秒速で探す命令書）
sql_query = """
SELECT text_content, author_name
FROM quotes
WHERE author_name = 'Albert Einstein'
"""

# ４．PANDAS CONVERT（SQLの探索結果を一瞬でバーチャルExcelシートに変換）
df_einstein = pd.read_sql_query(sql_query, conn)

print("---[EXTRACT RESULT] 倉庫から発掘されたアインシュタインの名言一覧 ---")
print(df_einstein)

# ５．REPORT EXPORT（成果物フォルダへ、行番号なしのキレイなExcelとして自動保存）
excel_output_path = os.path.join(output_dir, 'アインシュタイン限定_名言リサーチレポート.xlsx')
df_einstein.to_excel(excel_output_path, index=False)

# ６．PIPELINE CLOSE（ソリースの解放とパイプ切断）
conn.close()

print(f"\n🏆 SYS_STATUS: File 2 [ANALYZER & EXPORT] completed successfully")
print(f"📄 REPORT_PATH: {excel_output_path}")