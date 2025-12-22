import requests
import os

LINE_TOKEN = os.environ.get('LINE_CHANNEL_ACCESS_TOKEN')
LINE_USER_ID = os.environ.get('LINE_USER_ID')

def test_connection():
    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_TOKEN}"
    }
    data = {
        "to": LINE_USER_ID,
        "messages": [
            {
                "type": "text",
                "text": "成功です！PythonからLINEにメッセージが届きました！🎉"
            }
        ]
    }
    
    print("送信中...")
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        print("✅ 送信成功！スマホのLINEを確認してください。")
    else:
        print(f"❌ 送信失敗 (エラーコード: {response.status_code})")
        print(f"内容: {response.text}")

if __name__ == "__main__":
    test_connection()