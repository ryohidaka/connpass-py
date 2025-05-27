from connpass.client import Connpass


class TestConnpassInitialization:
    """Connpass クラスの初期化テスト"""

    def setup_method(self):
        """共通の事前設定"""
        self.dummy_key = "DUMMY_KEY"

    def create_connpass(self):
        return Connpass(self.dummy_key)

    def test_sets_api_key(self):
        """APIキーが正しく設定される"""
        connpass = self.create_connpass()
        assert connpass.api_key == self.dummy_key
