from ._base import db,Required,PrimaryKey,Set,Optional,uuid
from .bookCategory import BookCategory
from .author import BookAuthor
from .publisher import Publisher

class Book(db.Entity):
    _table_ = "tbl_book"
    idBook = PrimaryKey(uuid.UUID,default=uuid.uuid4,column='id_book')
    stock = Required(int)
    bookTitle = Required(str,column='book_title')
    bookCategory = Required(BookCategory,column='id_book_category')
    bookAuthor = Required(BookAuthor,column='id_book_author')
    bookPublisher = Required(Publisher,column='id_book_publisher')
    borrowedDetail = Set('BorrowedDetail')
    returnDetail = Set('ReturnDetail')
    picture = Optional(str)