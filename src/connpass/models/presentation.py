from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class PresentationType(str, Enum):
    """資料タイプ"""

    SLIDE = "slide"  # スライド
    MOVIE = "movie"  # 動画
    BLOG = "blog"  # ブログなど


class PresentationUser(BaseModel):
    """ユーザー"""

    id: int = Field(..., description="ユーザーID")
    nickname: str = Field(..., description="ニックネーム")


class Presentation(BaseModel):
    """資料"""

    user: Optional[PresentationUser] = Field(
        None, description="投稿者（資料を投稿したユーザー）"
    )
    url: str = Field(..., description="資料URL")
    name: str = Field(..., description="資料タイトル")
    presenter: Optional[PresentationUser] = Field(
        None, description="資料を発表したユーザー"
    )
    presentation_type: PresentationType = Field(..., description="資料タイプ")
    created_at: datetime = Field(..., description="投稿日時")


class GetEventPresentationsResponse(BaseModel):
    """イベント資料一覧のレスポンス"""

    results_returned: int
    results_available: int
    results_start: int
    presentations: List[Presentation]


class GetEventPresentationsQuery(BaseModel):
    """イベント資料一覧のパラメータ"""

    count: Optional[int] = Field(None, ge=1, le=100, description="取得件数（1〜100）")
    start: Optional[int] = Field(None, ge=1, description="取得開始位置（1〜）")
