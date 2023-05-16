from app.models import db
from app import responseHandler,requestStruct,requestMapping,email_regex
from flask import request
from json_checker import Checker
from uuid import uuid4
from flask_jwt_extended import jwt_required,get_jwt_identity

def listAuthors():
    try:
        # listBookAuthor = db.select(f"select a.id_book_author,a.name,a.email,a.gender,a.address,a.phone_number,b.id_book,b.stock,b.book_title,b.picture from tbl_book_author as a left join tbl_book as b on(a.id_book_author = b.id_book_author)")
        listBookAuthor = db.select(f"select id_book_author,name,email,gender,address,phone_number from tbl_book_author")
        data = []
        for i in listBookAuthor:
            data.append({
                "id": i[0],
                "name": i[1],
                "email": i[2],
                "gender": i[3],
                "address": i[4],
                "phoneNumber": i[5]
            })
        return responseHandler.ok(data)   
    except Exception as err:
        response = {
            "Error": str(err)
            }
        return responseHandler.badRequest(response)
   
@jwt_required()
def createAuthor():
    currentUser = get_jwt_identity()
    try:
        if currentUser['role'] == "Admin":
            jsonBody = request.json
            data = requestMapping.Authors(jsonBody)
            result = Checker(requestStruct.Authors(),soft=True).validate(data)
                
            #CHECK AUTHOR AND EMAIL IS EXIST OR NOT
            checkAuthor = db.select(f"select id_book_author from tbl_book_author where name = '{result['name']}' or email ='{result['email']}'")

            #CHECK RESULT IS NULL
            if result['name'] == "" or result['email'] == "" or result['gender'] == "" or result['address'] == "" or result['phoneNumber'] == ""  :
                response ={
                    "Message": "All Data Must be Filled"
                }
                return responseHandler.badRequest(response)
            
            if checkAuthor:
                response ={ 
                    "Message": "Author or Email Already Registered"
                }
                return responseHandler.badRequest(response)
            elif email_regex.match(jsonBody['email']) :
                createBookAuthor = (f"insert into tbl_book_author(id_book_author,name,email,gender,address,phone_number) values('{str(uuid4())}','{result['name']}','{result['email']}','{result['gender']}','{result['address']}','{result['phoneNumber']}')")
                db.execute(createBookAuthor)
                response={
                    "Data": jsonBody,
                    "Message": "Data Created"
                }
                return responseHandler.ok(response)
            elif not email_regex.match(jsonBody['email']):
                response={ 
                    "Message": "Email Not Valid"
                }
                return responseHandler.badRequest(response)
        else:
            response = {
                "Message": "You are Not Allowed Here"
            }
            return responseHandler.badRequest(response)
    except Exception as err:
            response ={
                "Error": str(err)
            }
            return responseHandler.badGateway(response)
    
def readAuthor(id):
    try:
        readAuthorById = db.select(f"select id_book_author,name,email,gender,address,phone_number from tbl_book_author where id_book_author = '{id}'")
        data = []
        for i in readAuthorById:
            data.append({
                "idBookAuthor": i[0],
                "name": i[1],
                "email": i[2],
                "gender": i[3],
                "address": i[4],
                "phoneNumber": i[5]
            })
        if not data:
            response = {
                "Message": "No Data Found"
            }
            return responseHandler.badGateway(response)
        response = {
            "Data": data[0]
        }
        return responseHandler.ok(response)
    except Exception as err:
        response = {
            "Error": str(err)
        }
        return responseHandler.badGateway(response)
    
@jwt_required()
def updateAuthor(id):
    currentUser = get_jwt_identity()
    try:
        if currentUser['role'] == "Admin":
            jsonBody = request.json
            data = requestMapping.Authors(jsonBody)
            result = Checker(requestStruct.userUpdate(),soft=True).validate(data)
            updateBookAuthor = (f"update tbl_book_author set name='{result['name']}', email='{result['email']}',gender='{result['gender']}',address='{result['address']}',phone_number='{result['phoneNumber']}' where id_book_author = '{id}'")
            db.execute(updateBookAuthor)
            response = {
                "Data": updateBookAuthor,
                "Message": "Success Update Author"
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
def deleteAuthor(id):
    currentUser = get_jwt_identity()
    try:
        if currentUser['role'] == "Admin":
            selectById = (f"select id_book_author from tbl_book_author where id_book_author = '{id}'")
            data=[]
            for i in db.execute(selectById):
                    data.append({
                    "id_book_author": i[0]
                })
            if not data:
                response = {
                    "message": "Data Not Found"
                }
                return responseHandler.badRequest(response)
            elif data:
                deleteById = (f"delete from tbl_book_author where id_book_author = '{id}'")
                db.execute(deleteById) 
                response = { 
                    "Message": "Delete Success"
                } 
                return responseHandler.ok(response)
            else:
                response = { 
                    "Message": "Delete invalid"
                } 
                return responseHandler.badRequest(response)
        else:
            response = {
                "Message": "You are Not Allowed Here"
            }
            return responseHandler.badRequest(response)
    except Exception as err:
            response={
                "Error": str(err)
            }
            return responseHandler.badGateway(response)    
    

