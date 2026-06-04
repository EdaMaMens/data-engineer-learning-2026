import requests
from bs4 import  BeautifulSoup

print("===Week 1 Day 3: Web Scraping * for Loop Combined ===\n")

# ==========================================================
# １．INPUT (WEBサイトから生データを要求してダウンロード)
# ==========================================================
target_url = "https://example.com"
response = requests.get(target_url)

# BaautifulSoupで解析可能なスープ構造にする
soup = BeautifulSoup(response.text, 'html.parser')

# ===============================================================
# ２．PROCESS * LOOP （ページ内の対象要素を『すべて』見つけてループ処理）
# ===============================================================
# 💡 予測通りのしいパーツ：ページ内にあるすべての 'p'（段落）要素ｗｐ「残さず全部見つける（find_all）」
# 取り出されたデータは、自動的に[段落1, 段落2, 段落3...]という「リスト型」の塊になります。
all_paragraphs = soup.find_all("p")

# 先ほどマスターした for 文の動線を、スクレイピングデータに結線する
# 「 paragraphs（段落の塊リスト）の中から、1つの paragraph（段落）を順番に取り出してこい」
for paragraph in all_paragraphs:

    # 取り出した要素から、魔法の扉（f""）を使って文字（.text）だけを画面に出力する
    print(f"📡 [EXTRACT_LOOP] 引っこ抜いた段落の文字: {paragraph.text}")
    print("-" * 30) # 区切り線を引いて見やすくする

print("n\🏆 SYS_STATUS: Scraping loop pipeline completed successfully.")
