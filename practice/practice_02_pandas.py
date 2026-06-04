import pandas as pd

# 寄り実践的な練習
data = {
    '日付':['2026-06-01', '2026-06-02', '2026-06-03', '2026-06-04'],
    '案件名': ['E邸外壁塗装', 'Fマンション点検', 'G戸建てアフター', 'Hビル修繕'],
    '金額': [450000, 125000, 80000, 670000],
    '分類': ['工事','点検','アフター','工事']
}

df = pd.DataFrame(data)

print("=== 全データ ===")
print(df)

# 実践的な操作
print("\n=== 金額の合計 ===")
print(df['金額'].sum())

print("\n=== 工事案件のみ抽出 ===")
print(df[df['分類'] == '工事'])

print("\n=== 金額順に並び替え ===")
print(df.sort_values('金額', ascending=False))

#ファイル保存
df.to_excel('案件一覧_2026年6月.xlsx', index=False)
print("\n✅ Excelファイルとして保存しました！")