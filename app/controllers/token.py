from flask_jwt_extended import jwt_required,get_jwt_identity,create_access_token
from flask import jsonify
from itsdangerous import URLSafeTimedSerializer
from app import app


@jwt_required(refresh = True)
def refresh():
    currentUser = get_jwt_identity()
    accessToken = create_access_token(identity=currentUser,fresh=True)
    return jsonify(accessToken = accessToken)

def generateToken(email):
    serializer = URLSafeTimedSerializer(app.config)