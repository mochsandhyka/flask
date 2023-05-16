from ._base import db,Required,PrimaryKey,Set,uuid

class BookCategory(db.Entity):
    _table_ = "tbl_book_category"
    idBookCategory = PrimaryKey(uuid.UUID,default=uuid.uuid4,column='id_book_category')
    category = Required(str, unique=True)
    book = Set('Book')