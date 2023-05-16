from app import app
from app.controllers import auth,user,books,authors,publisher,category,transaction,token

#AUTHOR
app.route('/list/authors',methods = ['GET'])(authors.listAuthors)
app.route('/create/author',methods = ['POST'])(authors.createAuthor)
app.route('/read/author/<id>',methods = ['GET'])(authors.readAuthor)
app.route('/update/author/<id>',methods = ['PATCH'])(authors.updateAuthor)
app.route('/delete/author/<id>',methods = ['DELETE'])(authors.deleteAuthor)


#PUBLISHER
app.route('/list/publishers',methods = ['GET'])(publisher.listPublisher)
app.route('/create/publisher',methods = ['POST'])(publisher.createPublisher)
app.route('/read/publisher/<id>',methods = ['GET'])(publisher.readPublisher)
app.route('/update/publisher/<id>',methods = ['PATCH'])(publisher.updatePublisher)
app.route('/delete/publisher/<id>',methods = ['DELETE'])(publisher.deletePublisher)


#CATEGORY
app.route('/list/categories',methods = ['GET'])(category.listCategory)
app.route('/create/category',methods = ['POST'])(category.createCategory)
app.route('/read/category/<id>',methods = ['GET'])(category.readCategory)
app.route('/update/category/<id>',methods = ['PATCH'])(category.updateCategory)
app.route('/delete/category/<id>',methods = ['DELETE'])(category.deleteCategory)


#BOOK
app.route('/list/books',methods = ['GET'])(books.listBooks)
app.route('/create/book',methods = ['POST'])(books.createBook)
app.route('/read/book/<id>',methods = ['GET'])(books.readBook)
app.route('/update/book/<id>',methods = ['PATCH'])(books.updateBook)
app.route('/delete/book/<id>',methods = ['DELETE'])(books.deleteBook)

#USER
app.route('/list/users',methods = ['GET'])(user.listUsers)
app.route('/create/user',methods = ['POST'])(user.createUser)
app.route('/read/user/<id>',methods = ['GET'])(user.readUser)
app.route('/update/user',methods = ['PATCH'])(user.updateUser)
app.route('/delete/user/<id>',methods = ['DELETE'])(user.deleteUser)


#AUTH
app.route('/auth/login',methods = ['POST'])(auth.login)
app.route('/auth/logout',methods = ['DELETE'])(auth.logout)

#TOKEN
app.route('/refresh',methods = ['POST'])(token.refresh)

#TRANSACTION
#BORROW
app.route('/list/booked',methods = ['GET'])(transaction.listBooked)
app.route('/list/approved',methods = ['GET'])(transaction.listApproved)
app.route('/list/book',methods = ['GET'])(transaction.listBook)
app.route('/borrow/<idBook>',methods = ['POST'])(transaction.borrowBook)
app.route('/list/accbook',methods = ['GET'])(transaction.listAccBook)
app.route('/accbook/<id>',methods = ['PATCH'])(transaction.accBook)
#RETURN
app.route('/list/return',methods = ['GET'])(transaction.listReturnBook)
app.route('/return/<id>',methods = ['POST'])(transaction.returnBook)
app.route('/list/charge',methods = ['GET'])(transaction.lateCharge)