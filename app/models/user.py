from ._base import db,Required,PrimaryKey,Set,date,Optional,uuid

class User(db.Entity):
    _table_ = "tbl_user"
    idUser = PrimaryKey(uuid.UUID,default=uuid.uuid4,column='id_user')
    username = Required(str,unique = True)
    email = Required(str,unique = True)
    password = Required(str)
    name = Required(str)
    gender = Required(str)
    address = Required(str)
    city = Required(str)
    phoneNumber = Required(str,column='phone_number')
    dateRegister = Required(date,column='date_register')
    picture = Optional(str,nullable = True)
    role = Required(str)
    borrowedbook = Set('BorrowedBook')
    returnbook= Set('ReturnBook')