class Blueprint:
    def __init__(self, prefix_url):
        self.routes = {}
        self.template = None
        self.prefix_url = prefix_url

    def route(self, path):
        if path in self.routes:
            raise AssertionError("Such route already exists.")

        def wrapper(handler):
            self.routes[self.prefix_url+path] = handler
            return handler

        return wrapper


