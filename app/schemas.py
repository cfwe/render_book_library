from pydantic import BaseModel, ConfigDict
from datetime import date, datetime
from typing import Optional

# APIリクエスト/レスポンスの共通ベースモデル
class BookBase(BaseModel):
    isbn: str
    title: str
    author: Optional[str] = None
    publisher: Optional[str] = None
    page_count: Optional[int] = None
    size: Optional[str] = None
    purchase_date: Optional[date] = None
    purchase_price: Optional[int] = None
    condition: Optional[str] = None
    summary: Optional[str] = None
    market_price: Optional[int] = None
    list_price: Optional[int] = None

# 書籍作成時に使用するスキーマ (リクエストボディ)
class BookCreate(BookBase):
    condition: Optional[str] = None
    summary: Optional[str] = None
    market_price: Optional[int] = None
    list_price: Optional[int] = None

# 書籍更新時に使用するスキーマ (リクエストボディ)
# ISBNはユニークキーであり、通常更新しないため除外
class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    publisher: Optional[str] = None
    page_count: Optional[int] = None
    size: Optional[str] = None
    purchase_date: Optional[date] = None
    purchase_price: Optional[int] = None
    condition: Optional[str] = None
    summary: Optional[str] = None
    market_price: Optional[int] = None
    list_price: Optional[int] = None

# 書籍読み取り時に使用するスキーマ (レスポンスボディ)
class Book(BookBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

# 価格情報取得APIのレスポンススキーマ
class PriceInfo(BaseModel):
    market_price: Optional[int] = None
    list_price: Optional[int] = None
