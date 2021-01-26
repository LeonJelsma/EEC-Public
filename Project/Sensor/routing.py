METHODS = ['POST', 'GET', 'PUT', 'PATCH', 'DELETE']


class Request:

    def __init__(self, request_data=None):
        self.raw_data = request_data
        self.method = None
        self.host = None
        self.form = None
        self.endpoint = None
        self.parse_request()

    def parse_request(self):
        if self.raw_data is not None:
            lines = self.raw_data.splitlines()
            method = lines[0][:7]
            for method_ in METHODS:
                if method_ in method:
                    self.method = method_
                    break
            self.host = lines[1][6:]
            target = lines[0].split(' ')
            self.endpoint = target[1]
            form = {}
            if self.method == 'POST':
                form_data = lines[-1]
                if '&' not in form_data:
                    entry = form_data.split('=')
                    if len(entry) > 1:
                        form[entry[0]] = entry[1]
                else:
                    pairs = form_data.split('&')
                    for pair in pairs:
                        entry = pair.split('=')
                        form[entry[0]] = entry[1]
                self.form = form

    def __str__(self):
        return {
            # 'raw_data': self.raw_data,
            'method': self.method,
            'host': self.host,
            'form': self.form,
            'endpoint': self.endpoint
        }


class _Route(object):
    def __init__(self, function, endpoint='', methods=[]):
        self.function = function
        self.endpoint = endpoint
        self.methods = methods

    def __call__(self, *args, **kwargs):
        for kwarg in kwargs:
            if isinstance(kwarg, Request):
                self.function(kwarg)
                break

        for arg in args:
            if isinstance(arg, Request):
                self.function(arg)
                break

    def handle_request(self, request: Request):
        response = self.function(request)
        if response is None:
            # TODO add actual status code
            return '200'
        else:
            return response


def Route(function=None, endpoint='', methods=[]):
    if function:
        return _Route(function)
    else:
        def wrapper(function):
            return _Route(function=function, endpoint=endpoint, methods=methods)

        return wrapper


class Router:

    def __init__(self):
        self.sensor = None
        self.routes = []

    def add_route(self, route: Route):
        self.routes.append(route)

    def set_sensor(self, sensor):
        self.sensor = sensor

    def handle_request(self, request: Request):
        for route in self.routes:
            if route.endpoint == request.endpoint:
                return route.handle_request(request)
        else:
            print('Route not found')
            return '404'
