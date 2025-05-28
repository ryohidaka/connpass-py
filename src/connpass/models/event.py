from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class EventOrder(int, Enum):
    """検索結果の表示順"""

    UPDATED_AT = 1  # 更新日時順
    STARTED_AT = 2  # 開催日時順
    CREATED_AT = 3  # 新着順


class EventType(str, Enum):
    """イベント参加タイプ"""

    PARTICIPATION = "participation"  # connpassで参加受付あり
    ADVERTISEMENT = "advertisement"  # 告知のみ


class OpenStatus(str, Enum):
    """イベントの開催状態"""

    PREOPEN = "preopen"  # 開催前
    OPEN = "open"  # 開催中
    CLOSE = "close"  # 終了
    CANCELLED = "cancelled"  # 中止


class Group(BaseModel):
    """グループ"""

    id: int = Field(..., description="グループID")
    subdomain: str = Field(..., description="サブドメイン")
    title: str = Field(..., description="グループ名")
    url: str = Field(..., description="グループのconnpass.com上のURL")


class ConnpassEvent(BaseModel):
    """イベント"""

    id: int = Field(..., description="イベントID")
    title: str = Field(..., description="イベント名")
    catch: str = Field(..., description="キャッチ")
    description: str = Field(..., description="概要")
    url: str = Field(..., description="connpass.com上のURL")
    image_url: str = Field(..., description="イベント画像URL")
    hash_tag: str = Field(..., description="X(Twitter)のハッシュタグ")
    started_at: datetime = Field(..., description="イベント開催日時")
    ended_at: datetime = Field(..., description="イベント終了日時")
    limit: Optional[int] = Field(None, description="定員")
    event_type: EventType = Field(..., description="イベント参加タイプ")
    open_status: OpenStatus = Field(..., description="イベントの開催状態")
    group: Optional[Group] = Field(None, description="グループ情報")
    address: Optional[str] = Field(None, description="開催場所")
    place: Optional[str] = Field(None, description="開催会場")
    lat: Optional[str] = Field(None, description="開催会場の緯度")
    lon: Optional[str] = Field(None, description="開催会場の経度")
    owner_id: int = Field(..., description="管理者のID")
    owner_nickname: str = Field(..., description="管理者のニックネーム")
    owner_display_name: str = Field(..., description="管理者の表示名")
    accepted: int = Field(..., description="参加者数")
    waiting: int = Field(..., description="補欠者数")
    updated_at: datetime = Field(..., description="更新日時")


class GetEventsResponse(BaseModel):
    """イベント一覧のレスポンス"""

    results_returned: int
    results_available: int
    results_start: int
    events: List[ConnpassEvent]


class GetEventsQuery(BaseModel):
    """イベント一覧のパラメータ"""

    event_id: Optional[List[int]] = Field(None, description="イベントID（複数指定可）")
    keyword: Optional[List[str]] = Field(
        None, description="キーワード(AND)（複数指定可）"
    )
    keyword_or: Optional[List[str]] = Field(
        None, description="キーワード(OR)（複数指定可）"
    )
    ym: Optional[List[str]] = Field(None, description="イベント開催年月（例: 201204）")
    ymd: Optional[List[str]] = Field(
        None, description="イベント開催年月日（例: 20120406）"
    )
    nickname: Optional[List[str]] = Field(None, description="参加者のニックネーム")
    owner_nickname: Optional[List[str]] = Field(
        None, description="管理者のニックネーム"
    )
    group_id: Optional[List[int]] = Field(None, description="グループID")
    subdomain: Optional[List[str]] = Field(None, description="サブドメイン")
    prefecture: Optional[List[str]] = Field(None, description="都道府県")
    order: Optional[EventOrder] = Field(
        None, description="表示順（1: 更新日時順, 2: 開催日時順, 3: 新着順）"
    )
    count: Optional[int] = Field(None, ge=1, le=100, description="取得件数（1〜100）")
    start: Optional[int] = Field(None, ge=1, description="取得開始位置（1〜）")
