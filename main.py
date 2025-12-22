import os
import requests
import hashlib
from bs4 import BeautifulSoup

# GitHub Secretsから読み込む設定
LINE_TOKEN = os.environ.get('LINE_CHANNEL_ACCESS_TOKEN')
LINE_USER_ID = os.environ.get('LINE_USER_ID')

# 監視したいURL（ここにあなたの監視したいURLを入れてください）
TARGET_URL = "https://www.toyota-ct.ac.jp/examinee/expenses/scholarship/" 

def send_line_message(text):
    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_TOKEN}"
    }
    data = {
        "to": LINE_USER_ID,
        "messages": [{"type": "text", "text": text}]
    }
    requests.post(url, headers=headers, json=data)

def main():
    # 1. サイト情報の取得
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(TARGET_URL, headers=headers)
        response.encoding = response.apparent_encoding # 文字化け防止
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        # 2. 監視範囲の特定
        # 豊田高専のサイトのメインコンテンツ部分（<main>タグ内）に絞る
        main_content = soup.find("main")
        
        if main_content:
            # 余計な空白や改行を整理してテキスト化
            current_content = main_content.get_text(strip=True)
        else:
            # 万が一mainタグがない場合は全体を見る
            current_content = soup.get_text(strip=True)
        
        # コンテンツのハッシュ値を作成
        current_hash = hashlib.md5(current_content.encode()).hexdigest()

        # 3. 前回の状態と比較
        hash_file = "last_hash.txt"
        last_hash = ""
        if os.path.exists(hash_file):
            with open(hash_file, "r") as f:
                last_hash = f.read()

        if current_hash != last_hash:
            print("更新を検知しました！")
            send_line_message(f"サイトが更新されました！\n{TARGET_URL}")
            # 新しいハッシュを保存
            with open(hash_file, "w") as f:
                f.write(current_hash)
        else:
            print("更新はありません。")

    except Exception as e:
        print(f"エラー発生: {e}")

if __name__ == "__main__":
    main()