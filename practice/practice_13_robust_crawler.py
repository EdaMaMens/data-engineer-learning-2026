import time
import requests
from bs4 import BeautifulSoup

# 複数ページのURLリスト（昨日検証した無限巡回対象に意図的にエラーURLを１本混入）
urls = [
    "https://scraping-for-beginner.herokuapp.com/udemy",  # 正常ページ
    "https://scraping-for-beginner.herokuapp.com/error_page",  # 存在しないエラーページ（検証用）
    "https://scraping-for-beginner.herokuapp.com/login"  # 正常ページ
]

for url in urls:
    print(f"START WALKING: {url}")

    try:
        # １．データの仕入れ（Extract）
        response = requests.get(url, timeout=5)
        # ステータスコードが4xx/5xx（404 Not Found等）の場合に明示的に例外を発生させる
        response.raise_for_status()

        # ２．パース処理（Transform）
        soup = BeautifulSoup(response.text, "html.parser")
        print(f"SUCCESS: {response.status_code}")

    except requests.exceptions.RequestException as e:
        # ★エラーを検知したらログを吐いて、安全に次のURLへスキップ（配管のバイパス）
        print(f"ERROR DETECTED [SKIP]: {e}")
        continue

    # サーバー負荷軽減のためのインターバル（一秒待機）
    time.sleep(1)

print("\nALL PROCESS FINISHED WITH EXIT CODE 0")