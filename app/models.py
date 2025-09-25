from sqlalchemy import Column, Integer, String, Date, Text, TIMESTAMP
from sqlalchemy.sql import func

from .database import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    isbn = Column(String(13), unique=True, nullable=False, index=True)
    title = Column(String(255), nullable=False)
    author = Column(String(255))
    publisher = Column(String(255))
    page_count = Column(Integer)
    size = Column(String(50))
    purchase_date = Column(Date)
    purchase_price = Column(Integer)
    condition = Column(String(50))
    summary = Column(Text)
    market_price = Column(Integer)
    list_price = Column(Integer)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())