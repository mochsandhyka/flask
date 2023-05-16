from app.models import db
from app import responseHandler
from uuid import uuid4
from flask_jwt_extended import jwt_required,get_jwt_identity


@jwt_required()
def listBooked():
    currentUser = get_jwt_identity()
    try:
        if currentUser['role'] == "User":
            selectBookedBook = db.select(f"select b.loan_date,c.book_title from tbl_detail_borrowed_book as a left join tbl_borrowed_book as b on (a.id_book_borrowed = b.id_book_borrowed) left join tbl_book as c on (a.id_book = c.id_book) where b.id_user = '{currentUser['idUser']}' and b.status = False")
            data = []
            for i in selectBookedBook:
                data.append({
                    "loanDate": i[0],
                    "bookTitle": i[1],
                })
            return responseHandler.ok(data)
        else:
            response ={
                "Message": "You are Not Allowed Here"
            }
            return responseHandler.badRequest(response)
    except Exception as err:
            response = {
                "Error": str(err)
            }
            return responseHandler.badGateway(response)    
   
    
@jwt_required()
def listApproved():
    currentUser = get_jwt_identity()
    try:
        if currentUser['role'] == "User":
            listBooked = db.select(f"select id_book_borrowed,loan_date from tbl_borrowed_book where status = True and id_book_borrowed not in(select id_book_borrowed from tbl_return_book)")
            data = []
            for i in listBooked:
                data.append({
                    "id": i[0],
                    "loanDate": i[1]
                })
            return responseHandler.ok(data)
        else:
            response ={
                "Message": "You are Not Allowed Here"
            }
            return responseHandler.badRequest(response)
    except Exception as err:
            response = {
                "Error": str(err)
            }
            return responseHandler.badGateway(response)   

@jwt_required()
def listBook():
    currentUser = get_jwt_identity()
    try:
        if currentUser['role'] == "User":    
            selectBook = db.select(f"select a.id_book,a.book_title,a.stock,b.id_book_author,b.name,c.id_book_publisher,c.name,d.id_book_category,d.category from tbl_book as a left join tbl_book_author as b on(a.id_book_author = b.id_book_author) left join tbl_book_publisher as c on(a.id_book_publisher = c.id_book_publisher) left join tbl_book_category as d on (a.id_book_category = d.id_book_category) where id_book not in(select a.id_book from tbl_detail_borrowed_book as a left join tbl_borrowed_book as b on (a.id_book_borrowed = b.id_book_borrowed) where id_user = '{id}') or id_book in (select a.id_book from tbl_detail_return_book as a left join tbl_return_book as b on (a.id_book_return = b.id_book_return) where id_user = '{currentUser['idUser']}') and stock > 0")
            data = []
            for i in selectBook:
                data.append({
                    "idBook": i[0],
                    "bookTitle": i[1],
                    "stock": i[2],
                    "idAuthor": i[3],
                    "author": i[4],
                    "idPublisher": i[5],
                    "publisher": i[6],
                    "idCategory": i[7],
                    "category": i[8]
                })
            if data:
                return responseHandler.ok(data)
            else:
                response = {
                    "Message": "You Already Borrowed this Book"
                }
                return responseHandler.badRequest(response)
        else:
            response = {
                "Message": "You are Not Allowed Here"
            }
            return responseHandler.badRequest(response)
    except Exception as err:
            response = {
                "Error": str(err)
            }
            return responseHandler.badGateway(response)
       

@jwt_required()
def borrowBook(idBook):
    currentUser = get_jwt_identity()
    try:
        if currentUser['role'] == "User":
            limit = 3
            bookedLimit = db.select(f"select id_book_borrowed from tbl_borrowed_book where id_book_borrowed not in (select id_book_borrowed from tbl_return_book) and id_user = '{currentUser['role']}'")
            data = []
            for i in bookedLimit:
                data.append(i)
            if len(data) >= limit:
                response={
                  "Message": "You Already borrow 3 Book"
                }
                return responseHandler.badRequest(response)
            else:
                myId = str(uuid4())
                db.execute(f"insert into tbl_borrowed_book(id_book_borrowed,loan_date,date_of_return,status,id_user) values ('{myId}',NOW(),NOW() + INTERVAL '7 DAYS','false','{id}')")
                db.execute(f"insert into tbl_detail_borrowed_book(id_borrowed_detail,id_book_borrowed,id_book) values('{str(uuid4())}','{myId}','{idBook}')")
                response={
                    "Message": "Please Wait Admin to Acc"
                }
                return responseHandler.ok(response)
        else:
            response = {
                "Message": "You are Not Allowed Here"
            }
            return responseHandler.badRequest(response)
    except Exception as err:
            response = {
                "Error": str(err)
            }
            return responseHandler.badGateway(response)   

@jwt_required()
def listAccBook():
    currentUser = get_jwt_identity() 
    try:
        if currentUser['role'] == "Admin":
            listBooked = db.select(f"select *from tbl_borrowed_book where status = False")
            data = []
            for i in listBooked:
                data.append({
                    "id": i[0],
                    "loanDate": i[1],
                    "dateReturn": i[2],
                    "status": i[3],
                    "idUser": i[4]
                })
            return responseHandler.ok(data)
        else:
            response = {
                "Message": "You are Not Allowed Here"
            }
            return responseHandler.badRequest(response)
    except Exception as err:
        response = {
            "Error": str(err)
        }
        return responseHandler.badGateway(response)
    
@jwt_required()
def accBook(id):
    currentUser = get_jwt_identity() 
    if currentUser['role'] == "Admin":
        try:
            #Update Status
            db.execute(f"update tbl_borrowed_book set status = True where id_book_borrowed = '{id}'")
            #Update Stock Book
            db.execute(f"update tbl_book tbl1 set stock = (stock - 1) from tbl_detail_borrowed_book tbl2 where tbl1.id_book = tbl2.id_book and id_book_borrowed = '{id}'")
            
            response ={
                "Message":"Book Approved"
            }
            return responseHandler.ok(response)
        except Exception as err:
            response = {
                "Error": str(err)
            }
            return responseHandler.badGateway(response)
    else:
        response = {
                "Message": "You are Not Allowed Here"
            }
        return responseHandler.badRequest(response)    
       

@jwt_required()
def listReturnBook():
    currentUser = get_jwt_identity() 
    try:
        if currentUser['role'] == "Admin":
            listReturnBook = db.select(f"select id_book_borrowed,loan_date,date_of_return,id_user from tbl_borrowed_book where id_book_borrowed not in(select id_book_borrowed from tbl_return_book)")
            data = []
            for i in listReturnBook:
                data.append({
                    "idBookBorrowed": i[0],
                    "loanDate": i[1],
                    "dateReturn": i[2],
                    "idUser": i[3]
                })
            return responseHandler.ok(data)
        else:
            response = {
                "Message": "You are Not Allowed Here"
            }
            return responseHandler.badRequest(response)
    except Exception as err:
        response = {
            "Error": str(err)
        }
        return responseHandler.badGateway(response)
    

@jwt_required()
def returnBook(id):
    currentUser = get_jwt_identity() 
    try:
        if currentUser['role'] == "Admin":
            myId = str(uuid4())
            charge = 300
            select = db.execute(f"select extract(day from date_of_return)-extract(day from now()),a.id_user,a.id_book_borrowed,b.id_book from tbl_borrowed_book as a left join tbl_detail_borrowed_book as b on(a.id_book_borrowed = b.id_book_borrowed) where a.id_book_borrowed = '{id}' ")
            for i in select:
                data = {
                    "dateReturn": i[0],
                    "idUser": i[1],
                    "idBookBorrowed": i[2],
                    "idBook": i[3]
                }
            if data['dateReturn'] > 0:
                data['dateReturn'] = 0
            else:
                data['dateReturn'] = data['dateReturn']

            late_charge = data['dateReturn'] * charge

            db.execute(f"insert into tbl_return_book (id_book_return,return_date,late_charge,id_user,id_book_borrowed) values ('{myId}',NOW(),'{late_charge}','{data['idUser']}','{data['idBookBorrowed']}')")
            db.execute(f"insert into tbl_detail_return_book(id_return_detail,id_book_return,id_book) values ('{str(uuid4())}','{myId}','{data['idBook']}')")
            db.execute(f"update tbl_book set stock = (stock + 1) where id_book = '{data['idBook']}'")
            
            response = {
                "Message" : "Book is Returned"
            }
            return responseHandler.ok(response)
        else:
            response = {
                "Message": "You are Not Allowed Here"
            }
            return responseHandler.badRequest(response)
    except Exception as err:
        response = {
            "Error": str(err)
        }
        return responseHandler.badGateway(response)
    
@jwt_required()
def lateCharge():
    currentUser = get_jwt_identity() 
    if currentUser['role'] == "Admin":
        try:
            lateCharge = db.select(f"select id_book_return,late_charge from tbl_return_book")
            data = []
            for i in lateCharge:
                data.append({
                    "idBookReturn": i[0],
                    "lateCharge": i[1]
                })
            return responseHandler.ok(data)
        except Exception as err:
            response = {
                "Error": str(err)
            }
            return responseHandler.badRequest(response)
    else:
        response = {
            "Message": "You are Not Allowed Here"
        }
    return responseHandler.badRequest(response)
