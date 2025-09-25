from fastapi import FastAPI, Depends, HTTPException, Response, status, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from pathlib import Path
from typing import List
import unicodedata

from . import crud, models, schemas
from . import rakuten
from .database import SessionLocal, engine
from .services import book_lookup, market_price_scraper

app = FastAPI()

# テンプレートファイルのディレクトリを絶対パスで指定
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(Path(BASE_DIR, 'templates')))

# APIリクエストごとにデータベースセッションを生成し、処理完了後に閉じるための依存関係
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=Response)
def read_root(request: Request, db: Session = Depends(get_db)):
    books = crud.get_books(db, skip=0, limit=100)
    # ブラウザのキャッシュを無効にするためのヘッダーを追加
    response = templates.TemplateResponse("index.html", {"request": request, "books": books})
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

@app.get("/api/lookup_book/{isbn}", response_model=schemas.BookCreate)
async def lookup_book_info(isbn: str):
    isbn = unicodedata.normalize('NFKC', isbn) # 正規化
    book_info = await book_lookup.lookup_book_info_by_isbn(isbn)
    if book_info is None:
        raise HTTPException(status_code=404, detail="Book not found in any external source")
    return book_info

@app.get("/api/books/", response_model=List[schemas.Book])
def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    books = crud.get_books(db, skip=skip, limit=limit)
    return books


@app.get("/api/prices/{isbn}", response_model=schemas.PriceInfo)
async def get_prices_for_isbn(isbn: str):
    """
    指定されたISBNの中古価格と定価をBook-Off Onlineから取得する（データベース登録不要）。
    """
    isbn = unicodedata.normalize('NFKC', isbn) # 正規化
    prices = await market_price_scraper.scrape_bookoff_online_price(isbn)
    if prices is None:
        raise HTTPException(status_code=404, detail="Could not fetch prices from Book-Off Online for the given ISBN.")
    return prices


@app.get("/api/books/{isbn}/update_prices", response_model=schemas.Book)
async def update_prices_from_bookoff(isbn: str, db: Session = Depends(get_db)):
    """
    Book-Off Onlineから中古価格と定価を調査し、データベースを更新する
    """
    isbn = unicodedata.normalize('NFKC', isbn) # 正規化
    print("update_prices_from_bookoff called", isbn)
    db_book = crud.get_book_by_isbn(db, isbn=isbn)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    print("isbn:", db_book.isbn)
    prices = await market_price_scraper.scrape_bookoff_online_price(db_book.isbn)
    if prices is None:
        raise HTTPException(status_code=404, detail="Could not fetch prices from Book-Off Online.")

    # 取得した価格でDBを更新 (Noneでない方の値だけ更新される)
    update_data = schemas.BookUpdate(
        market_price=prices.get("market_price"), list_price=prices.get("list_price")
    )
    print( update_data.market_price, update_data.list_price )
    return crud.update_book(db, db_book, update_data)


@app.get("/api/books/{book_id}", response_model=schemas.Book)
def read_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book


@app.put("/api/books/{book_id}", response_model=schemas.Book)
def update_book_endpoint(
    book_id: int, book_in: schemas.BookUpdate, db: Session = Depends(get_db)
):
    db_book = crud.get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return crud.update_book(db=db, db_book=db_book, book_in=book_in)


@app.delete("/api/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book_endpoint(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    crud.delete_book(db=db, db_book=db_book)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.post("/api/books/", response_model=schemas.Book, status_code=201)
async def create_book_endpoint(book: schemas.BookCreate, db: Session = Depends(get_db)):
    book.isbn = unicodedata.normalize('NFKC', book.isbn) # 正規化
    db_book = crud.get_book_by_isbn(db, isbn=book.isbn)
    if db_book:
        raise HTTPException(status_code=400, detail="ISBN already registered")

    # 書籍登録時に価格情報を取得してセットする
    prices = await market_price_scraper.scrape_bookoff_online_price(book.isbn)
    if prices:
        book.market_price = prices.get("market_price")
        book.list_price = prices.get("list_price")

    return crud.create_book(db=db, book=book)
