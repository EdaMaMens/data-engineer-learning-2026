import pandas as pd
import os
from datetime import datetime

print("=== Week 1 Day 2: データの入力・処理・出力を完全分離した統合パイプライン ===\n")

# ====================================================
# 0. 環境認識（足元の住所を確認する）
# ====================================================
# このスクリプト（practice_04_file_merge.py）が置いてある「practice」フォルダの絶対パスを取得
current_dir = os.path.dirname(os.path.abspath(__file__))

# ====================================================
# 1. 入力（Input）: 専用の「data」部屋から生データを自動読込
# ====================================================
# 「data」フォルダの住所と、その中にあるCSVファイルの住所を結合（結線）
data_dir = os.path.join(current_dir, 'data')
info_path = os.path.join(data_dir, 'summary_june.csv')
sales_path = os.path.join(data_dir, 'sales_june.csv')

# 安全装置：読み込むべき生データが指定の場所に存在するか偵察
if not os.path.exists(info_path) or not os.path.exists(sales_path):
    print(f"❌ エラー: 『data』フォルダの中に必要なCSVファイルが見つかりません。")
    print(f"探した住所: {data_dir}")
    print("【対処】practice/data/ の中に2つのCSVがあるか確認してください。")

else:
    # 住所が正しければ、Pandasの工具箱でバーチャルExcel（DataFrame）に変換して読み込む
    df_info = pd.read_csv(info_path)
    df_sales = pd.read_csv(sales_path)

    print("📥 [入力完了] 外部CSVデータの自動読み込みに成功しました。")

    # ====================================================
    # 2. 処理（Process）: 表の合流（マージ）と、条件に沿ったくり抜き
    # ====================================================
    # 共通の「プロジェクトID」の列を噛み合わせて、2つの表を正確に1本に合流させる
    df_merged = pd.merge(df_info, df_sales, on='プロジェクトID')

    # 合流したデータから、契約金額が3,000,000円以上の「大型案件」だけをくり抜く（フィルタリング）
    df_high_value = df_merged[df_merged['契約金額'] >= 3000000]

    print("⚙️  [処理完了] データの結合、および300万円以上の大型案件の抽出を行いました。")

    # ====================================================
    # 3. 出力（Output）: 「成果物」部屋を自動建築してレポートを保存
    # ====================================================
    # 「成果物」という名前の出力専用フォルダの住所を組み立てる
    output_dir = os.path.join(current_dir, '成果物')

    # 【自動建築ロジック】もし指定した住所に「成果物」フォルダが無ければ、その場で作る
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"📁 フォルダ自動建築: 『成果物』ディレクトリを新規作成しました。")

    # 「成果物」フォルダの中に保存するExcelファイルの最終的な住所を決定
    output_path = os.path.join(output_dir, '統合売上レポート_2026年6月.xlsx')

    # Excelファイルとして出力（左端の不要な行番号インデックスは非表示）
    df_high_value.to_excel(output_path, index=False)

    print(f"\n🏆 [完全完了] すべての処理が破綻なく成功しました！")
    print(f"最終成果物の保存先: {output_path}")
    print(f"システム実行時刻: {datetime.now()}")