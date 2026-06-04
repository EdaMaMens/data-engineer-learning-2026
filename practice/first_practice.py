import pandas as pd
from datetime import datetime

# === 最初の練習：建築・住宅関連データをイメージした自動処理 ===

# サンプルデータ（あなたの経験を活かしたイメージ）
data = {
    'プロジェクト名': ['A邸新築', 'B戸建てリフォーム', 'Cマンション修繕', 'D邸アフター'],
    '契約金額(万円)': [4500, 2800, 1650, 320],
    'ステータス': ['設計中', '施工中', '完了', 'アフター'],
    '開始日': ['2026-01-15', '2026-02-01', '2025-11-10', '2026-03-01'],
    '担当者': ['えだまめ', '田中', '佐藤', 'えだまめ']
}

# DataFrameに変換
df = pd.DataFrame(data)

# --- ここから実践的な処理 ---
print("=== 住宅プロジェクト一覧 ===")
print(df)

# 条件でフィルタリング
print("\n=== アフター案件のみ抽出 ===")
after_cases = df[df['ステータス'] == 'アフター']
print(after_cases)

# 金額の集計
print("\n=== 合計契約金額 ===")
total = df['契約金額(万円)'].sum()
print(f"総額: {total:,} 万円")

# 日付型に変換して分析準備
df['開始日'] = pd.to_datetime(df['開始日'])

# CSVとして保存（成果物）
df.to_csv('projects_summary.csv', index=False, encoding='utf-8-sig')
print("\nprojects_summary.csv として保存しました！")

print(f"\n✅ 完了時間: {datetime.now()}")