def User():
    schema = {
        "username": str,
        "email": str,
        "password": str,
        "name": str,
        "gender": str,
        "address": str,
        "city": str,
        "phoneNumber": str,
        "role": str
    }
    return schema

def userUpdate():
    schema = {
        "username": str,
        "email": str,
        "password": str,
        "name": str,
        "gender": str,
        "address": str,
        "city": str,
        "phoneNumber": str
    }
    return schema


def Books():
    schema = { 
        # "stock": int,
        "bookTitle": str,
        "bookCategory": str,
        "bookAuthor": str,
        "bookPublisher": str
    }
    return schema

def Authors():
    schema = { 
        "name": str,
        "email": str,
        "gender": str,
        "address": str,
        "phoneNumber": str

    }
    return schema

def Publisher():
    schema = {
        "name": str,
        "email": str,
        "address": str,
        "phoneNumber": str
    }
    return schema

def Category():
    schema = {
        "category": str
    }
    return schema