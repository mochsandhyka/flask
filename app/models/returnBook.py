from ._base import db,Required,PrimaryKey,Set,Optional,uuid,date
from .user import User
from .borrowedBook import BorrowedBook

class ReturnBook(db.Entity):
    _table_ = "tbl_return_book"
    idBookReturn = PrimaryKey(uuid.UUID,default=uuid.uuid4,column='id_book_return')
    returnDate = Required(date,column='return_date')
    lateCharge = Optional(int,column='late_charge')
    user = Required(User,column='id_user')
    borrowed = Required(BorrowedBook,column='id_book_borrowed')
    returnDetail = Set('ReturnDetail')


