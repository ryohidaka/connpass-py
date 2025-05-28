"""イベント一覧取得のサンプル"""

import os

from connpass import Connpass


def main():
    # クライアントを初期化
    API_KEY = os.environ["API_KEY"]
    client = Connpass(api_key=API_KEY)

    # イベント一覧を取得
    response = client.get_events()

    # イベント情報を出力
    for event in response.events:
        print(f"[{event}] {event.title} @ {event.place}")
        print(f"URL: {event.url}")
        print(f"参加者数: {event.accepted}人 / 状態: {event.open_status}")
        print("-" * 60)


main()
