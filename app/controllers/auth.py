from app.models import db
from app import responseHandler
from flask import request,jsonify
import hashlib,os
from flask_jwt_extended import create_refresh_token,create_access_token,get_jwt_identity,unset_access_cookies,jwt_required


def login():
    try:
        jsonBody = request.json
        hashpassword = hashlib.md5((jsonBody['password']+os.getenv("SALT_PASSWORD")).encode())
        user = db.select(f"select id_user,role from tbl_user where username = '{jsonBody['username']}' and password = '{hashpassword.hexdigest()}' ")
        for i in user:
            userAuth = {
                "idUser": i[0],
                "role": i[1]
            }
        if user:
            accessToken = create_access_token(identity=userAuth,fresh=True)
            refreshToken = create_refresh_token(identity=user)
            response = {
                "Data": userAuth,
                "accessToken": accessToken,
                "refreshToken": refreshToken,
                "Message": "Login Success"}
            #set_access_cookies(jsonify(response), access_token)
            return responseHandler.ok(response)
        else:
            response ={
                "Message": "Username / Password is invalid"
            }
            return responseHandler.badRequest(response)
    except Exception as err:
        response ={
            "Error": str(err)
        }
        return responseHandler.badGateway(response)
    
@jwt_required()
def logout():
    try:
        currentUser = get_jwt_identity()
        if currentUser:
            response = {
                "Message": "Logout Successfull"
            }
            unset_access_cookies(jsonify(response))
            return responseHandler.ok(response)
        else:
            response = {
                "Message": "Logout Unccessfull"
            }
            return responseHandler.badRequest(response)
    except Exception as err:
        response = {
                "Error": str(err)
            }
        return responseHandler.badGateway(response)
    