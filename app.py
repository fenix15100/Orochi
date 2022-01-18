import os

from werkzeug import run_simple
from orochi import Orochi
from BookController import BookController
from webob import Request, Response

app = Orochi(port=8000,
             debug=True,
             static_files={
                 '/static': os.path.join(os.path.dirname(__file__), 'static')
             })


@app.route("/home/{name}")
def home(request: Request, response: Response, name: str):
    response.text = '<html><script src="http://localhost:8000/static/script.js"></script></html>'
    return response


app.register_blueprint(BookController)

if __name__ == "__main__":
    run_simple('localhost',
               port=app.port,
               application=app,
               use_reloader=True if app.debug else False,
               use_debugger=app.debug,
               static_files=app.static_files
               )
