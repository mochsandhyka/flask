from ._base import db,PrimaryKey,uuid,Required,Optional,Set

class BookAuthor(db.Entity):
    _table_ = "tbl_book_author"
    idBookAuthor = PrimaryKey(uuid.UUID,default=uuid.uuid4,column='id_book_author')
    name = Required(str, unique=True)
    email = Optional(str)
    gender = Optional(str)
    address = Optional(str)
    phoneNumber = Optional(str,column='phone_number')
    book = Set('Book')