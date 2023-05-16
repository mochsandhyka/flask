from flask import Flask
from flask_jwt_extended import JWTManager 
import os,uuid,re
from flask_cors import CORS
from pony.flask import Pony
from pony.orm import Database
from .models._base import db
from datetime import datetime,timedelta

app = Flask(__name__)

#JWT
JWTManager(app)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
#app.config['JWT_ACCESS_TOKEN_EXPIRES'] = os.getenv('JWT_ACCESS_TOKEN_EXPIRES')
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
app.config['JWT_COOKIE_CSRF_PROTECT'] = os.getenv('JWT_COOKIE_CSRF_PROTECT')


#UPLOAD
app.config['UPLOAD_FOLDER_BOOKS'] = os.getenv("UPLOAD_FOLDER_BOOKS")
app.config['UPLOAD_FOLDER_USERS'] = os.getenv("UPLOAD_FOLDER_USERS")
app.config['MAX_CONTENT_LENGHT'] = os.getenv("MAX_CONTENT_LENGHT")
app.config['ALLOWED_EXTENSIONS'] = os.getenv("ALLOWED_EXTENSION")
allowedextensions = app.config['ALLOWED_EXTENSIONS']
uploadFolderBooks = app.config['UPLOAD_FOLDER_BOOKS']
uploadFolderUsers = app.config['UPLOAD_FOLDER_USERS']



#DB
db__params = {'provider': os.getenv('DB_PROVIDER'),
             'user': os.getenv('DB_USER'),
             'password': os.getenv('DB_PASSWORD'),
             'host': os.getenv('DB_HOST'),
             'database': os.getenv('DB_NAME')}

#PONY
Pony(app)

#CORS
CORS(app)

#GENERATE ID
def generateId():
    myId = uuid.uuid4
    return myId

#EMAIL REGEX
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
email_regex = re.compile(r"[^@]+@[^@]+\.[^@]")


from app import routes
if __name__ == "__main__":
    app.run()
