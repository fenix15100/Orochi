from webob import Request, Response

from orochi.blueprint import Blueprint

BookController = Blueprint(prefix_url="/book")

@BookController.route("/{id}")
def getBooks(request: Request, response: Response,id):
    response.text = "BOOKSCONTROLLER"+id
    return response
