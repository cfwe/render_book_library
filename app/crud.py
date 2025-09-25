from sqlalchemy.orm import Session

from . import models, schemas


def get_book_by_isbn(db: Session, isbn: str):
    return db.query(models.Book).filter(models.Book.isbn == isbn).first()


def get_books(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Book).offset(skip).limit(limit).all()


def get_book(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()


def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.Book(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def update_book(db: Session, db_book: models.Book, book_in: schemas.BookUpdate):
    # Pydanticモデルから辞書に変換。Noneの項目は除外する
    update_data = book_in.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_book, key, value)

    db.commit()
    db.refresh(db_book)
    return db_book


def delete_book(db: Session, db_book: models.Book):
    db.delete(db_book)
    db.commit()