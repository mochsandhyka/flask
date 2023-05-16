def User(jsonBody):
    data = {
        "username": jsonBody['username'],
        "email": jsonBody['email'],
        "password": jsonBody['password'],
        "name": jsonBody['name'],
        "gender": jsonBody['gender'],
        "address": jsonBody['address'],
        "city": jsonBody['city'],
        "phoneNumber": jsonBody['phoneNumber'],
        "role": jsonBody['role']
    }
    return data

def userUpdate(jsonBody):
    data = {
        "username": jsonBody['username'],
        "email": jsonBody['email'],
        "password": jsonBody['password'],
        "name": jsonBody['name'],
        "gender": jsonBody['gender'],
        "address": jsonBody['address'],
        "city": jsonBody['city'],
        "phoneNumber": jsonBody['phoneNumber']
    }
    return data

def Books(jsonBody):
    data={
        # "stock": jsonBody['stock'],
        "bookTitle": jsonBody['bookTitle'],
        "bookCategory": jsonBody['bookCategory'],
        "bookAuthor": jsonBody['bookAuthor'],
        "bookPublisher": jsonBody['bookPublisher'],
    } 
    return data

def Authors(jsonBody):
    data = { 
        "name": jsonBody['name'],
        "email": jsonBody['email'],
        "gender": jsonBody['gender'],
        "address": jsonBody['address'],
        "phoneNumber": jsonBody['phoneNumber']
    }
    return data

def Publisher(jsonBody):
    data = {
        "name": jsonBody['name'],
        "email": jsonBody['email'],
        "address": jsonBody['address'],
        "phoneNumber": jsonBody['phoneNumber']
    }
    return data

def Category(jsonBody):
    data = {
        "category": jsonBody['category']
    }
    return data