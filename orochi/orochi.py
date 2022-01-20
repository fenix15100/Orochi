from http import HTTPStatus
from webob import Request, Response
from .route import Route


class Orochi:

    def __init__(self, debug=False, port=8000, static_files=None):
        self._routes = []
        self.debug = debug
        self.port = port
        self.static_files = static_files
        self._blueprints = []

    def __call__(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_request(request)

        return response(environ, start_response)

    def dispatch_request(self, request: Request):
        response = Response()
        for route in self._routes:
            route: Route = route
            match, parsed_parameters = route.match(request_path=request.path)
            if match:
                handler, error = route.handle_request(request, response)
                if error is None:
                    return handler(request, response, **parsed_parameters)
                else:
                    return self.error_response(response=response, http_status=error)

            else:
                return self.error_response(response=response, http_status=HTTPStatus.NOT_FOUND)

    @classmethod
    def error_response(cls, response: Response, http_status: HTTPStatus, message=None):
        response.status_code = http_status.value
        response.text = f"<h1><b>{str(http_status.value)} {http_status.phrase} {http_status.description}</b></h1></br" \
                        f"><p>{message if message is not None else ''}</p> "
        return response

    def route(self, path: str, methods=None):
        def wrapper(handler: callable):
            self.add_route(pattern=path, handler=handler, methods=methods)
            return handler

        return wrapper

    def add_route(self, pattern: str, handler: callable, methods=None) -> None:
        route = [r for r in self._routes if r.__str__() == pattern]
        assert len(route) == 0, f"Ruta duplicada: {pattern}"
        self._routes.append(Route(path_pattern=pattern, handler=handler, methods=methods))
