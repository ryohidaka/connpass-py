"""イベント資料一覧取得のサンプル"""

import os

from connpass import Connpass


def main():
    # クライアントを初期化
    API_KEY = os.environ["API_KEY"]
    client = Connpass(api_key=API_KEY)

    # イベント資料一覧を取得
    response = client.get_event_presentations(364)
    presentations = response.presentations

    # 資料情報を出力
    for presentation in presentations:
        print(presentation.name)


main()
