import pytest
import requests_mock

from connpass import Connpass
from connpass.models import PresentationType
from tests.utils import load_mock_response


class TestGetEventPresentations:
    """イベント資料一覧を取得のテスト"""

    base_url = "https://connpass.com/api/v2"

    def setup_method(self):
        self.api_key = "DUMMY_KEY"
        self.client = Connpass(self.api_key)

    def test_get_events_success(self):
        """正常にイベントの資料一覧を取得できる"""
        mock_url = f"{self.base_url}/events/364/presentations"
        mock_response = load_mock_response("tests/testdata/event-presentations.json")

        with requests_mock.Mocker() as m:
            m.get(mock_url, json=mock_response)
            response = self.client.get_event_presentations(364)

            # メタ情報の検証
            assert response.results_returned == 1
            assert response.results_available == 91
            assert response.results_start == 1

            # イベント資料本体の検証
            presentation = response.presentations[0]

            assert presentation.name == "Togetterまとめ"
            assert presentation.url == "https://togetter.com/li/294875"

            # 投稿者情報
            assert presentation.user is not None
            assert presentation.user.id == 8
            assert presentation.user.nickname == "haru860"

            # 発表者者情報
            assert presentation.presenter is not None
            assert presentation.presenter.id == 8
            assert presentation.presenter.nickname == "haru860"

            # Enum フィールド
            assert presentation.presentation_type == PresentationType.BLOG

            # 日付型であること、および値の妥当性
            assert presentation.created_at.year == 2012
            assert presentation.created_at.month == 4
            assert presentation.created_at.tzinfo is not None

    def test_get_events_403_error(self):
        """403エラー時に例外を発生させる"""
        mock_url = f"{self.base_url}/events/364/presentations"

        with requests_mock.Mocker() as m:
            m.get(mock_url, status_code=403, reason="Forbidden")

            with pytest.raises(ValueError) as excinfo:
                self.client.get_event_presentations(364)

            assert "403 Forbidden" in str(excinfo.value)
