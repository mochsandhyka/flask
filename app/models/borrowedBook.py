from ._base import db,Required,PrimaryKey,Set,Optional,uuid,date
from .user import User 

class BorrowedBook(db.Entity):
    _table_ = "tbl_borrowed_book"
    idBookBorrowed = PrimaryKey(uuid.UUID,default=uuid.uuid4,column='id_book_borrowed')
    loanDate = Required(date,column='loan_date')
    dateOfReturn = Optional(date,column='date_of_return')
    status = Required(bool)
    user = Required(User,column='id_user')
    borrowedDetail = Set('BorrowedDetail')
    returnBook = Set('ReturnBook')
