import time
import requests
from bs4 import BeautifulSoup

# 検証用URL（503エラーが起きてもリトライで粘る配管をテスト）
urls = [
    "https://scraping-for-beginner.herokuapp.com/udemy",
    "https://www.python.org/"  # 確実に200 OKが返る、検証用の正常サイト
]

MAX_RETRY = 3  # 最大リトライ回数

for url in urls:
    print(f"\nSTART WALKING: {url}")

    # 各URLごとに成功フラグとリトライグループを管理
    success = False

    for retry_count in range(1, MAX_RETRY + 1):
        try:
            # １．データの仕入れ（タイムアウトを短めに設定してテスト）
            response = requests.get(url, timeout=3)
            response.raise_for_status()

            # ２．パース処理
            soup = BeautifulSoup(response.text, "html.parser")
            print(f"SUCCESS: {response.status_code} (Attempt: {retry_count})")

            success = True
            break  # 成功したらリトライループ（内部のfor文）を抜ける

        except requests.exceptions.RequestException as e:
            print(f"ATTEMPT {retry_count} FAILED: {e}")
            if retry_count < MAX_RETRY:
                print("Waiting 2 seconds before next retry...")
                time.sleep(2)  # 2秒待機して次のリトライへ
            else:
                print("MAX RETRIES REACHED. GIVING UP THIS URL.")
    # リトライを尽くしても失敗した場合はスキップして次のURLへ
    if not success:
        print(f"SKIP URL: {url}")
        continue
    # URL間のインターバル
    time.sleep(1)

print("\nALL PROCESS FINISHED WITH EXIT CODE 0")