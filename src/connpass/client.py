from typing import Optional

from connpass.core import RequestHandler
from connpass.models import (
    GetEventPresentationsQuery,
    GetEventPresentationsResponse,
    GetEventsQuery,
    GetEventsResponse,
)

from .constants import BASE_URL


class Connpass:
    """Connpass API クライアント。

    - [APIリファレンス](https://connpass.com/about/api/v2/#section/%E6%A6%82%E8%A6%81/%E8%AA%8D%E8%A8%BC)

    Attributes:
        api_key (str): Connpass API キー。
    """

    def __init__(self, api_key: str):
        """Connpassクライアントを初期化する。

        Args:
            api_key (str): Connpass APIキー。

        Example:
            c = Connpass("YOUR_API_KEY")
        """
        self.api_key = api_key

        # 共通リクエストハンドラーを呼び出し
        self.request_handler = RequestHandler(api_key=api_key, base_url=BASE_URL)

    def get_events(self, query: Optional[GetEventsQuery] = None) -> GetEventsResponse:
        """
        検索クエリの条件に応じたイベント一覧を取得する。

        Args:
            query (Optional[GetEventsQuery]): 検索条件

        Returns:
            GetEventsResponse: イベント一覧レスポンス

        Raises:
            ValueError: API リクエストに失敗した場合
        """
        query_dict = query.model_dump(exclude_none=True) if query else None
        response_json = self.request_handler.get("events", query_dict)
        return GetEventsResponse(**response_json)

    def get_event_presentations(
        self, id: int, query: Optional[GetEventPresentationsQuery] = None
    ) -> GetEventPresentationsResponse:
        """
        イベントに投稿された資料一覧を取得する。

        Args:
            query (Optional[GetEventPresentationsQuery]): 検索条件

        Returns:
            GetEventPresentationsResponse: イベント資料一覧のレスポンス

        Raises:
            ValueError: API リクエストに失敗した場合
        """
        query_dict = query.model_dump(exclude_none=True) if query else None
        response_json = self.request_handler.get(
            f"events/{id}/presentations", query_dict
        )
        return GetEventPresentationsResponse(**response_json)
