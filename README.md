# connpass-py

![PyPI - Version](https://img.shields.io/pypi/v/connpass)
[![codecov](https://codecov.io/gh/ryohidaka/connpass-py/graph/badge.svg?token=wdfk9DbTO5)](https://codecov.io/gh/ryohidaka/connpass-py)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

Python 用 connpass API v2 クライアント

## インストール

```bash
pip install connpass
```

## 使用例

> [!IMPORTANT]
> すべての API エンドポイントでは、API キーによる認証が必須です。
>
> API キーの発行には[ヘルプページ](https://help.connpass.com/api/)での利用申請が必要です。

### クライアントの初期化

```py
from connpass import Connpass

API_KEY = "<YOUR_API_KEY>"

client = Connpass(api_key=API_KEY)
```

### イベント

```py
response = client.get_events()
events = response.events
```

### イベント資料

```py
response = client.get_event_presentations(364)
presentations = response.presentations
```

## リンク

- [API リファレンス](https://connpass.com/about/api/v2/)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
