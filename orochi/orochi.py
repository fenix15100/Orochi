import inspect
import os

from parse import parse
from webob import Request, Response

from blueprint import Blueprint
from .route import Route


class Orochi:

    def __init__(self, debug=False, port=8000, static_files=None):
        self._routes = {}
        self.debug = debug
        self.port = port
        self.static_files = static_files
        self.blueprints = []

    def __call__(self, environ, start_response):
        request = Request(environ)
        response = self.handle_request(request)

        return response(environ, start_response)

    def handle_request(self, request: Request):
        response = Response()
        handler, kwargs = self.find_handler(request_path=request.path)
        if handler is not None:
            if inspect.isclass(handler):
                handler = getattr(handler(), request.method.lower(), None)

                if handler is None:
                    raise AttributeError("Method now allowed", request.method)

            return handler(request, response, **kwargs)
        else:
            return self.default_response(response)

    def find_handler(self, request_path):
        for path, handler in self._routes.items():
            parse_result = parse(path, request_path)
            if parse_result is not None:
                return handler, parse_result.named
        return None, None

    def default_response(self, response: Response):
        response.status_code = 404
        response.text = "Not found."
        return response

    def route(self, path):
        if path in self._routes:
            raise AssertionError("Such route already exists.")

        def wrapper(handler):
            self._routes[path] = handler
            return handler

        return wrapper

    def add_route(self, pattern, handler, methods=None):
        """ Add a new route """
        assert pattern not in self._routes
        self._routes[pattern] = Route(path_pattern=pattern, handler=handler, methods=methods)

    def register_blueprint(self, blueprint: Blueprint):
        self.blueprints.append(blueprint)
        self._routes = dict(**self._routes, **blueprint.routes)
