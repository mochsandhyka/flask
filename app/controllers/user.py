from app.models import db
from app import requestMapping,requestStruct,responseHandler,email_regex,os,uploadFolderUsers,allowedextensions
from flask import request
from json_checker import Checker
from uuid import uuid4
import hashlib
from flask_jwt_extended import jwt_required,get_jwt_identity
from werkzeug.utils import secure_filename

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowedextensions

def listUsers():
    try:
        listUsers = db.select(f"select id_user,username,email,password,name,gender,address,city,phone_number,date_register,picture,role from tbl_user")
        data = []
        for i in listUsers:
            data.append({
                "idUser": i[0],
                "username": i[1],
                "email": i[2],
                "password": i[3],
                "name": i[4],
                "gender": i[5],
                "address": i[6],
                "city": i[7],
                "phoneNumber":i[8],
                "dateRegister":i[9],
                "picture": i[10],
                "role": i[11]
            })
        return responseHandler.ok(data)
    except Exception as err:
        response = {
            "Error": str(err)
        }
        return responseHandler.badGateway(response)
    
@jwt_required(fresh=True)
def createUser():
    currentUser = get_jwt_identity()
    try:
        if currentUser['role'] == "Admin":    
            jsonBody = request.json
            data = requestMapping.User(jsonBody)
            result = Checker(requestStruct.User(),soft=True).validate(data)
            checkUser = db.select(f"select *from tbl_user where username = '{jsonBody['username']}' or email = '{jsonBody['email']}'")

            if jsonBody['username'] =="" or jsonBody['email'] =="" or jsonBody['password'] =="" or jsonBody['name'] =="" or jsonBody['gender'] =="" or jsonBody['address'] == "" or jsonBody['city'] =="" or jsonBody['phoneNumber'] =="" or jsonBody['role'] =="":
                response = {
                    "Message": "All Data Must be Filled"
                }
                return responseHandler.badRequest(response)
            if checkUser:
                response = {
                    "Message": (f" Username : '{jsonBody['username']}' or Email : '{jsonBody['email']}' is Exist ")
                }
                return responseHandler.badRequest(response)
            else:
                password = result['password']
                hashpassword = hashlib.md5((password+ os.getenv("SALT_PASSWORD")).encode())
                createUser = (f"insert into tbl_user(id_user,username,email,password,name,gender,address,city,phone_number,date_register,picture,role) values('{str(uuid4())}','{result['username']}','{result['email']}','{hashpassword.hexdigest()}','{result['name']}','{result['gender']}','{result['address']}','{result['city']}','{result['phoneNumber']}',now(),'{'default.jpg'}','{result['role']}')")
                db.execute(createUser)
                response = {
                    "Data": jsonBody,
                    "Message": "Data Created"
                }
                return responseHandler.ok(response)
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

@jwt_required()
def readUser(id):
    currentUser = get_jwt_identity()
    if currentUser['idUser'] == id:
        try:
            get_jwt_identity()
            readById = db.select(f"select id_user,username,email,password,name,gender,address,city,phone_number,date_register,picture,role from tbl_user where id_user = '{id}'" )
            data = []
            for i in readById:
                data.append({
                    "idUser": i[0],
                    "username":i[1],
                    "email": i[2],
                    "password": i[3],
                    "name": i[4],
                    "gender": i[5],
                    "address": i[6],
                    "city": i[7],
                    "phoneNumber":i[8],
                    "dateRegister":i[9],
                    "picture":i[10],
                    "role":i[11]
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
    else:
        response = {
            "Message": "You are Not Allowed Here"
        }
        return responseHandler.badRequest(response)

@jwt_required()
def updateUser():
    currentUser = get_jwt_identity()
    if currentUser['role'] == "User":
        jsonBody = request.form
        files = request.files.getlist('picture')
        data = requestMapping.userUpdate(jsonBody)
        result = Checker(requestStruct.userUpdate(),soft=True).validate(data)
        hashpass = hashlib.md5((result['password']+os.getenv("SALT_PASSWORD")).encode())
        try:
            checkUsername = db.select(f"select username from tbl_user where username = '{result['username']}' and username != (select username from tbl_user where id_user = '{currentUser['idUser']}')")
            checkEmail = db.select(f"select email from tbl_user where email = '{result['email']}' and email != (select email from tbl_user where id_user = '{currentUser['idUser']}')")
            if checkUsername:
                response = {
                    "Message": "User is exist"
                }
                return responseHandler.badRequest(response)
            elif checkEmail:
                response = {
                    "Message": "Email is exist"
                }
                return responseHandler.badRequest(response)
            if result['username'] =="" or result['email'] =="" or result['password'] =="" or result['name'] =="" or result['gender'] =="" or result['address'] == "" or result['city'] =="" or result['phoneNumber'] =="":
                response = {
                    "Message": "All Data Must be Filled"
                }
                return responseHandler.badRequest(response)
            if email_regex.match(result['email']):
                for user in db.select(f"select id_user,picture from tbl_user where id_user = '{currentUser['idUser']}'"): 
                    user = {
                        "id_user": user[0],
                        "pic_user": user[1]
                    } 
                for i in files:
                    if i and allowed_file(i.filename):
                        try:
                            os.remove(os.path.join(uploadFolderUsers, user['pic_user']))
                        except:
                            pass
                        filename = secure_filename(i.filename)
                        picfilename = currentUser['idUser'] + '_' + filename
                        i.save(os.path.join(uploadFolderUsers,picfilename))
                        success = True
                    if success:
                        updateUser = (f"update tbl_user set username='{result['username']}' ,password = '{hashpass.hexdigest()}',email='{result['email']}',name='{result['name']}',gender='{result['gender']}',address='{result['address']}',city='{result['city']}',phone_number='{result['phoneNumber']}',picture = '{picfilename}' where id_user = '{currentUser['idUser']}'")
                        db.execute(updateUser)
                        response = {
                            "Data": updateUser,
                            "Message": "Success Update User"
                        }
                        return responseHandler.ok(response)
                if not files:
                    updateUser = (f"update tbl_user set username='{result['username']}' ,password = '{hashpass.hexdigest()}',email='{result['email']}',name='{result['name']}',gender='{result['gender']}',address='{result['address']}',city='{result['city']}',phone_number='{result['phoneNumber']}' where id_user = '{currentUser['idUser']}'")
                    db.execute(updateUser)
                    response = {
                        "Data": updateUser,
                        "Message": "Success Update User"
                    }
                    return responseHandler.ok(response)
            response = {
                "Message": "Email not Valid"
            }
            return responseHandler.badRequest(response)
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
def deleteUser(id):
    currentUser = get_jwt_identity()
    try:
        if currentUser['role'] == "Admin":    
            selectById = (f"select id_user from tbl_user where id_user = '{id}'")
            data = []
            for i in db.execute(selectById):
                data.append({
                    "idUser": i[0]
                })
            if not data:
                response = {
                    "Message": "Data Not Found"
                }
                return responseHandler.badRequest(response)
            elif data:
                deleteById = (f"delete from tbl_user where id_user = '{id}'")
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
    
