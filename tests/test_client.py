import pytest
import requests

from connpass.client import Connpass


class TestConnpassInitialization:
    """Connpass クラスの初期化テスト"""

    def setup_method(self):
        """共通の事前設定"""
        self.dummy_key = "DUMMY_KEY"
        self.base_url = "https://connpass.com/api/v2"

    @pytest.fixture(autouse=True)
    def patch_base_url(self, monkeypatch):
        monkeypatch.setattr("connpass.constants.BASE_URL", self.base_url)

    def create_connpass(self):
        return Connpass(self.dummy_key)

    def test_sets_api_key(self):
        """APIキーが正しく設定される"""
        connpass = self.create_connpass()
        assert connpass.api_key == self.dummy_key

    def test_creates_request_handler(self):
        """RequestHandlerが生成される"""
        connpass = self.create_connpass()
        handler = connpass.request_handler
        assert hasattr(handler, "get")
        assert handler.api_key == self.dummy_key
        assert handler.base_url == self.base_url
        assert isinstance(handler.client, requests.Session)
        assert handler.client.timeout == 10
