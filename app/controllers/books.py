from app.models import db
from app import requestMapping,requestStruct,responseHandler,allowedextensions,uploadFolderBooks
from flask import request
from json_checker import Checker
from uuid import uuid4
from flask_jwt_extended import jwt_required,get_jwt_identity
from werkzeug.utils import secure_filename
import os

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowedextensions

def listBooks():
    try:
        listBooks = db.select(f"select a.id_book,a.stock,a.book_title,a.id_book_category,a.id_book_author,a.id_book_publisher,a.picture,b.category,c.name,c.email,c.gender,c.address,c.phone_number,d.name,d.email,d.address,d.phone_number from tbl_book as a left join tbl_book_category as b on(a.id_book_category = b.id_book_category) left join tbl_book_author as c on(a.id_book_author = c.id_book_author) left join tbl_book_publisher as d on (a.id_book_publisher = d.id_book_publisher)")
        data = []
        for i in listBooks:
            data.append({
                "idBook": i[0],
                "stock": i[1],
                "bookTitle": i[2],
                "idBookCategory": i[3],
                "idBookAuthor": i[4],
                "idBookPublisher": i[5],
                "picture": i[6],
                "category": i[7],
                "authorName": i[8],
                "authorEmail": i[9],
                "authorGender": i[10],
                "authorAddress": i[11],
                "authorPhoneNumber": i[12],
                "publisherName": i[13],
                "publisherEmail": i[14],
                "publisherAddress": i[15],
                "publisherPhoneNumber": i[16]
            })
        return responseHandler.ok(data)
    except Exception as err:
        response = {
            "Error": str(err)
        }
        return responseHandler.badGateway(response)

@jwt_required()    
def createBook():
    currentUser = get_jwt_identity()
    try:
        if currentUser['role'] == "Admin":
            files = request.files.getlist('picture')
            jsonBody = request.form
            data = requestMapping.Books(jsonBody)
            result = Checker(requestStruct.Books(),soft=True).validate(data)
            checkBook = db.select(f"select *from tbl_book where book_title = '{result['bookTitle']}' and id_book_author = '{result['bookAuthor']}'")

            if result['stock'] == "" or result['bookTitle'] == "" or result['bookCategory'] == "" or result['bookAuthor'] == "" or result['bookPublisher'] == "":
                response = {
                    "Message": "All Data Must be Filled"
                }
                return responseHandler.badRequest(response)
            if checkBook:
                response = {
                    "Message": (f" Book '{jsonBody['bookTitle']}' is Exist ")
                }
                return responseHandler.badRequest(response)
            else:
                for i in files:
                    if i and allowed_file(i.filename):
                        filename = secure_filename(i.filename)
                        picfilename = str(uuid4()) + '_' + filename 
                        i.save(os.path.join(uploadFolderBooks,picfilename))
                        success = True
                    if success:
                        createBook = (f"insert into tbl_book(id_book,stock,book_title,id_book_category,id_book_author,id_book_publisher,picture) values ('{str(uuid4())}','{jsonBody['stock']}','{result['bookTitle']}','{result['bookCategory']}','{result['bookAuthor']}','{result['bookPublisher']}','{picfilename}')")
                        db.execute(createBook)
                        response = {
                            "Data": jsonBody,
                            "Message": "Data Created"
                        }
                        return responseHandler.ok(response)
                if not files:
                    picfilename = "book.jpg"
                    createBook = (f"insert into tbl_book(id_book,stock,book_title,id_book_category,id_book_author,id_book_publisher,picture) values ('{str(uuid4())}',{jsonBody['stock']},'{result['bookTitle']}','{result['bookCategory']}','{result['bookAuthor']}','{result['bookPublisher']}','{picfilename}')")
                    db.execute(createBook)
                    response={
                                "Data": createBook,
                                "Message": "Data Created"
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
       
def readBook(id):
    try:
        readById = db.select(f"select a.id_book,a.stock,a.book_title,a.id_book_category,a.id_book_author,a.id_book_publisher,a.picture,b.category,c.name,c.email,c.gender,c.address,c.phone_number,d.name,d.email,d.address,d.phone_number from tbl_book as a left join tbl_book_category as b on(a.id_book_category = b.id_book_category) left join tbl_book_author as c on(a.id_book_author = c.id_book_author) left join tbl_book_publisher as d on (a.id_book_publisher = d.id_book_publisher) where a.id_book = '{id}'")

        data = []
        for i in readById:
            data.append({
                "idBook": i[0],
                "stock": i[1],
                "bookTitle": i[2],
                "idBookCategory": i[3],
                "idBookAuthor": i[4],
                "idBookPublisher": i[5],
                "picture": i[6],
                "category": i[7],
                "authorName": i[8],
                "authorEmail": i[9],
                "authorGender": i[10],
                "authorAddress": i[11],
                "authorPhoneNumber": i[12],
                "publisherName": i[13],
                "publisherEmail": i[14],
                "publisherAddress": i[15],
                "publisherPhoneNumber": i[16]
            })
        if not data:
            response = {
                "Message": "Book Not Found"
            }
            return responseHandler.badRequest(response)
        response ={
            "Data": data[0]
        }
        return responseHandler.ok(response)
    except Exception as err:
        response = {
            "Error": str(err)
        }
        return responseHandler.badGateway(response)

@jwt_required() 
def updateBook(id):
    currentUser = get_jwt_identity()
    if currentUser['role'] == "Admin":
        try:
            jsonBody = request.json
            data = requestMapping.Books(jsonBody)
            result = Checker(requestStruct.userUpdate(),soft=True).validate(data)
            checkBook = db.select(f"select book_title from tbl_book where book_title = '{result['bookTitle']}' and book_title != (select book_title from tbl_book where id_book = '{id}')")
            if checkBook:
                response = {
                    "Message": "Book is Exist"
                }
                return responseHandler.badRequest(response)
            else:
                updateBook = (f"update tbl_book set stock = '{result['stock']}', book_title = '{result['bookTitle']}', id_book_category = '{result['bookCategory']}', id_book_author = '{result['bookAuthor']}', id_book_publisher = '{result['bookPublisher']}' where id_book = '{id}'")
                db.execute(updateBook)
                response = {
                    "Data": updateBook,
                    "Message": "Successs Update Book"
                }
                return responseHandler.ok(response)
        except Exception as err:
            response = {
                "Message": str(err)
            }
            return responseHandler.badGateway(response)
    else:
        response = {
            "Message": "You are Not Allowed Here"
        }
        return responseHandler.badRequest(response)

@jwt_required()
def deleteBook(id):
    currentUser = get_jwt_identity()
    try:
        if currentUser['role'] == "Admin":
            selectById = (f"select id_book from tbl_book where id_book = '{id}'")
            data = []
            for i in db.execute(selectById):
                data.append({
                    "idBook": i[0]
                }) 
            if not data:
                response ={
                    "Message": "Data Not Found"
                }
                return responseHandler.badRequest(response)
            elif data:
                deleteById = (f"delete from tbl_book where id_book = '{id}'")
                db.execute(deleteById)
                response = {
                    "Message": "Delete Success"
                }
                return responseHandler.ok(response)
            response = {
                "Message": "Delete Invalid"
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
    