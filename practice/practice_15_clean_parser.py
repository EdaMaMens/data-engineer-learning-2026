import sys
from bs4 import BeautifulSoup

# 検証用：ECサイトから取得したと想定される３パターンの模擬HTMLデータ
mock_html_list = [
    'div class="item">品名: マイク <span class="weight">176g</span><div>',  # パターン１: 正常データ
    'div class="item">品名: 不明スピーカー <span class="weight"></span><div>',  # パターン２: キーはあるが中身が空（空文字）
    'div class="item">品名: モニターアーム <div>'  # パターン３: そもそもクラス名 "weight" 自体が存在しない（欠損）
]

for index, html in enumerate(mock_html_list, start=1):
    print(f"\n--- PARSING DATASET {index} ---")
    soup = BeautifulSoup(html, "html.parser")

    # １．要素の検索・抽出の試み
    weight_element = soup.find(class_="weight")

    # ★重要:データベースにゴミをいれないための「仕分け配管」
    if weight_element is None:
        # パターン３を検知:そもそもタグが存在しない場合
        print("CRITICAL: 'weight' class not found in HTML. Setting default value.")
        cleaned_weight = 0
    elif weight_element.text.strip() == "":
        # パターン２を検知:タグはあるが文字が空っぽの場合
        print("WARNING: 'weight' text is empty. Setting default value.")
        cleaned_weight = 0
    else:
        # パターン１:正常にデータが存在する場合（文字列から「ｇ」を削って数値化）
        raw_text = weight_element.text  # "176g"
        cleaned_weight = int(raw_text.replace("g", ""))  # 文字列を整数型（Integer）に変換
        print("DATA CLEANING SUCCESSFUL.")

    # ２．最終的にデータベースへ流せる状態になった安全な値を出力
    print(f"FINAL DATABASE INPUT VALUE -> WEIGHT: {cleaned_weight} (Type: {type(cleaned_weight).__name__})")

print("\nALL PROCESS FINISHED WITH EXIT CODE 0")