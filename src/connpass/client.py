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
