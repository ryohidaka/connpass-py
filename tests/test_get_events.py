import pytest
import requests_mock

from connpass import Connpass
from connpass.models import EventType, GetEventsQuery, OpenStatus
from tests.utils import load_mock_response


class TestGetEvents:
    """イベント一覧を取得のテスト"""

    base_url = "https://connpass.com/api/v2"

    def setup_method(self):
        self.api_key = "DUMMY_KEY"
        self.client = Connpass(self.api_key)

    def test_get_events_success(self):
        """正常にイベント一覧を取得できる"""
        mock_url = f"{self.base_url}/events?keyword=BPStudy"
        mock_response = load_mock_response("tests/testdata/events.json")

        with requests_mock.Mocker() as m:
            m.get(mock_url, json=mock_response)

            query = GetEventsQuery(keyword=["BPStudy"])
            response = self.client.get_events(query)

            # メタ情報の検証
            assert response.results_returned == 1
            assert response.results_available == 1
            assert response.results_start == 1

            # イベント本体の検証
            event = response.events[0]
            assert event.id == 364
            assert event.title == "BPStudy#56"
            assert event.catch == "株式会社ビープラウドが主催するWeb系技術討論の会"
            assert "USクラウド最新動向勉強会" in event.description
            assert event.url == "https://bpstudy.connpass.com/event/364/"
            assert event.image_url.endswith(".png")
            assert event.hash_tag == "bpstudy"

            # 日付型であること、および値の妥当性
            assert event.started_at.year == 2012
            assert event.started_at.month == 4
            assert event.started_at.tzinfo is not None
            assert event.ended_at.hour == 20
            assert event.updated_at.year == 2014

            # Enum フィールド
            assert event.event_type == EventType.PARTICIPATION
            assert event.open_status == OpenStatus.CLOSE

            # グループ情報
            assert event.group is not None
            assert event.group.id == 1
            assert event.group.subdomain == "bpstudy"
            assert event.group.title == "BPStudy"
            assert event.group.url == "https://bpstudy.connpass.com/"

            # 会場情報
            assert event.address == "東京都港区北青山2-8-44"
            assert event.place == "先端技術館＠TEPIA"
            assert float(event.lat) == 35.672968
            assert float(event.lon) == 139.7169046

            # 管理者情報
            assert event.owner_id == 8
            assert event.owner_nickname == "haru860"
            assert event.owner_display_name == "佐藤 治夫"

            # 参加者情報
            assert event.accepted == 0
            assert event.waiting == 0

    def test_get_events_403_error(self):
        """403エラー時に例外を発生させる"""
        mock_url = f"{self.base_url}/events?keyword=BPStudy"

        with requests_mock.Mocker() as m:
            m.get(mock_url, status_code=403, reason="Forbidden")

            query = GetEventsQuery(keyword=["BPStudy"])
            with pytest.raises(ValueError) as excinfo:
                self.client.get_events(query)

            assert "403 Forbidden" in str(excinfo.value)
