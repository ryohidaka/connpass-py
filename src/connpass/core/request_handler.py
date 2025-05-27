from typing import Any, Dict, Optional
from urllib.parse import urlencode

import requests

from connpass.constants import DUMMY_USER_AGENT


class RequestHandler:
    """共通APIリクエストハンドラー"""

    def __init__(self, api_key: str, base_url: str):
        """RequestHandlerを初期化する。

        Args:
            api_key (str): APIキー。
            base_url (str): APIのベースURL。
        """
        self.api_key = api_key
        self.base_url = base_url
        self.client = requests.Session()
        self.client.timeout = 10  # 秒

    def get(self, endpoint: str, query: Optional[Dict[str, Any]] = None) -> Any:
        """指定されたエンドポイントに対してGETリクエストを送信し、レスポンスのJSONを返却する。

        Args:
            endpoint (str): APIのエンドポイント（相対パス）。
            query (Optional[Dict[str, Any]]): クエリパラメータの辞書。リスト型の値にも対応する。

        Returns:
            Any: JSONデコードされたレスポンスデータ。

        Raises:
            ValueError: リクエストエラーやHTTPステータスエラーが発生した場合。
        """
        url = f"{self.base_url}/{endpoint}"
        try:
            if query:
                query_string = urlencode(query, doseq=True)
                url = f"{url}?{query_string}"

            headers = {"X-API-Key": self.api_key, "User-Agent": DUMMY_USER_AGENT}
            response = self.client.get(url, headers=headers)

            if 400 <= response.status_code < 500:
                raise ValueError(
                    f"APIリクエストに失敗しました: {response.status_code} {response.reason}"
                )
            elif response.status_code >= 500:
                raise ValueError(
                    f"予期しないエラーが発生しました: {response.status_code} {response.reason}"
                )

            return response.json()

        except requests.RequestException as e:
            raise ValueError(f"APIリクエストに失敗しました: {str(e)}") from e
