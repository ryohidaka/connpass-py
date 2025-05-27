import pytest
from requests import RequestException

from connpass.core import RequestHandler


class DummyResponse:
    """レスポンスモック用のダミークラス"""

    def __init__(self, status_code=200, json_data=None, reason="OK"):
        self.status_code = status_code
        self._json_data = json_data or {}
        self.reason = reason

    def json(self):
        return self._json_data


@pytest.fixture
def handler():
    return RequestHandler(api_key="DUMMY_KEY", base_url="https://example.com/api")


def test_get_success(monkeypatch, handler):
    """正常にJSONを返却する"""

    def mock_get(url, headers):
        assert "X-API-Key" in headers
        return DummyResponse(json_data={"result": "ok"})

    monkeypatch.setattr(handler.client, "get", mock_get)

    result = handler.get("test-endpoint")
    assert result == {"result": "ok"}


def test_get_with_query(monkeypatch, handler):
    """クエリパラメータが正しくURLに付加される"""

    def mock_get(url, headers):
        assert "param1=value1" in url
        assert "param2=value2" in url
        return DummyResponse()

    monkeypatch.setattr(handler.client, "get", mock_get)

    handler.get("test-endpoint", query={"param1": "value1", "param2": "value2"})


def test_get_4xx_raises_value_error(monkeypatch, handler):
    """4xx エラーが ValueError を送出する"""

    def mock_get(url, headers):
        return DummyResponse(status_code=404, reason="Not Found")

    monkeypatch.setattr(handler.client, "get", mock_get)

    with pytest.raises(ValueError, match="APIリクエストに失敗しました"):
        handler.get("test-endpoint")


def test_get_5xx_raises_value_error(monkeypatch, handler):
    """5xx エラーが ValueError を送出する"""

    def mock_get(url, headers):
        return DummyResponse(status_code=503, reason="Service Unavailable")

    monkeypatch.setattr(handler.client, "get", mock_get)

    with pytest.raises(ValueError, match="予期しないエラーが発生しました"):
        handler.get("test-endpoint")


def test_get_request_exception(monkeypatch, handler):
    """通信エラーが ValueError を送出する"""

    def mock_get(url, headers):
        raise RequestException("Timeout")

    monkeypatch.setattr(handler.client, "get", mock_get)

    with pytest.raises(ValueError, match="APIリクエストに失敗しました: Timeout"):
        handler.get("test-endpoint")
