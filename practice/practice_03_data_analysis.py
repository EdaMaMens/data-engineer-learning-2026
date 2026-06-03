import pandas as pd
from datetime import datetime

print("=== Week 1 実践課題 03: データ分析練習 ===\n")

# より実践的な住宅関連データ
data = {
    'プロジェクトID': [101, 102, 103, 104, 105],
    '案件名': ['A邸新築', 'B戸建てリフォーム', 'Cマンション大規模修繕', 'D邸アフター対応', 'Eビル外壁工事'],
    '契約金額': [4800000, 2650000, 12500000, 450000, 3250000],
    '工期(日)': [150, 85, 240, 30, 95],
    'ステータス': ['設計中', '施工中', '完了', 'アフター', '施工中'],
    '開始日': ['2026-01-10', '2026-02-15', '2025-10-01', '2026-04-01', '2026-03-20']
}

df = pd.DataFrame(data)

# 日付をdatetime型に変換
df['開始日'] = pd.to_datetime(df['開始日'])

print("1. 全プロジェクト一覧")
print(df)

print("\n2. 契約金額の合計と平均")
print(f"総額: {df['契約金額'].sum():,} 円")
print(f"平均金額: {df['契約金額'].mean():,.0f} 円")

print("\n3. 施工中の案件のみ抽出")
print(df[df['ステータス'] == '施工中'])

print("\n4. 金額が高い順に並び替え（上位3件）")
print(df.sort_values('契約金額', ascending=False).head(3))

print("\n5. 工期が100日以上のプロジェクト")
print(df[df['工期(日)'] >= 100])

# 分析結果を保存
df.to_excel('住宅プロジェクト分析_2026.xlsx', index=False)
df.to_csv('住宅プロジェクト分析_2026.csv', index=False, encoding='utf-8-sig')

print("\n✅ 分析結果をExcelファイルとして保存しました！")
print(f"\n終了時間: {datetime.now()}")