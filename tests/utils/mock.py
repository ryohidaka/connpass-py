import json


def load_mock_response(file_path: str) -> dict:
    """モック用JSONレスポンスをファイルから読み込む"""
    with open(file_path, encoding="utf-8") as f:
        return json.load(f)
