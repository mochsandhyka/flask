from ._base import db,Required,PrimaryKey,Set,Optional,uuid
from .returnBook import ReturnBook
from .book import Book

class ReturnDetail(db.Entity):
    _table_ = "tbl_detail_return_book"
    idReturnDetail = PrimaryKey(uuid.UUID,default=uuid.uuid4,column='id_return_detail')
    returnBook = Required(ReturnBook, column='id_book_return')
    book = Required(Book, column='id_book')