from ._base import db,Required,PrimaryKey,uuid
from .borrowedBook import BorrowedBook
from .book import Book

class BorrowedDetail(db.Entity):
    _table_ = "tbl_detail_borrowed_book"
    idBorrowedDetail = PrimaryKey(uuid.UUID,default=uuid.uuid4,column='id_borrowed_detail')
    borrowedBook = Required(BorrowedBook, column='id_book_borrowed')
    book = Required(Book, column='id_book')