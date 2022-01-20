import os

from werkzeug import run_simple
from orochi import Orochi
from webob import Request, Response

app = Orochi(port=8000,
             debug=True,
             static_files={
                 '/static': os.path.join(os.path.dirname(__file__), 'static')
             })


@app.route("/home/{name}", methods=["GET", "POST"])
def home(request: Request, response: Response, name: str):
    if request.method == 'POST':
        print(request)
        response.json = request.json
    elif request.method == 'GET':
        response.text = name
    return response


if __name__ == "__main__":
    run_simple('localhost',
               port=app.port,
               application=app,
               use_reloader=True if app.debug else False,
               use_debugger=app.debug,
               static_files=app.static_files
               )
