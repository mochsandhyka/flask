from ._base import db,Required,PrimaryKey,Set,Optional,uuid

class Publisher(db.Entity):
    _table_ = "tbl_book_publisher"
    idBookPublisher = PrimaryKey(uuid.UUID,default=uuid.uuid4,column='id_book_publisher')
    name = Required(str, unique=True)
    email = Optional(str)
    address = Optional(str)
    phoneNumber = Optional(str,column='phone_number')
    book = Set('Book')