import asyncio
import json
import weakref
from aiohttp import web


class ResponseError(Exception):
    
    def __init__(self, response):
        super(NotFoundDevice, self).__init__()
        self.response = response


class EnvSenseWebApplication:

    device_types = {'sensor': {'manager': 'sensor_manager',
                               'error_prefix': '10'},
                    'actuator': {'manager': 'sensor_manager',
                                 'error_prefix': '20'},
                    'logic': {'manager': 'logic_manager',
                              'error_prefix': '30'}}

    def __init__(self, app, *args, **kwargs):
        self._app = weakref.ref(app)
        self.config = app.config.get('webserver', {})
        self.server = web.Application(*args, **kwargs)
        self.server.router.add_route('GET', '/', self.default_handler)

        self.server.router.add_route('GET', '/{device_type}', self.device_type_read_handler)
        self.server.router.add_route('GET', '/{device_type}/{name}', self.device_read_handler)

        self.server.router.add_route('GET', '/{device_type}/{name}/{var_name}', self.read_var_handler)
        self.server.router.add_route('PUT', '/{device_type}/{name}/{var_name}', self.write_var_handler)
        self.server.router.add_route('POST', '/{device_type}/{name}/{var_name}', self.call_handler)

    @property
    def app(self):
        return self._app()

    def error_response(self, error_msg, error_code, status):
        return web.Response(text=json.dumps({'errorMessage': error_msg,
                                             'errorCode': error_code}),
                            content_type='application/json',
                            status=status)

    def error_not_found_device(self, device_type, error_prefix, device_name):
        return self.error_response(error_msg="{} '{}' not found".format(device_type.capitalize(), device_name),
                                   error_code='{}001'.format(error_prefix),
                                   status=404)

    def error_not_found_attribute(self, device_type, error_prefix, device_name, var_name):
        return self.error_response(error_msg="{} '{}' does not have variable '{}'".format(device_type.capitalize(),
                                                                                          device_name,
                                                                                          var_name),
                                   error_code='{}002'.format(error_prefix),
                                   status=404)

    def get_device_type(self, request):
        device_type = request.match_info['device_type']

        if device_type not in self.device_types:
            return self.error_response(error_msg="Device type '{}' not found".format(device_type),
                                       error_code='00001',
                                       status=404)

        return device_type

    def get_device(self, device_type, device_name, error_prefix):
        manager = getattr(self.app, self.device_types[device_type]['manager'])
        try:
            device = manager.items[device_name]
            return device
        except KeyError:
            resp = self.error_not_found_device(device_type=device_type,
                                               error_prefix=error_prefix,
                                               sensor_name=device_name)
            raise ResponseError(resp)

    @asyncio.coroutine
    def default_handler(self, request):
        return web.Response(text=json.dumps({'deviceTypes': list(self.device_types.keys())}),
                            content_type='application/json',
                            status=200)

    @asyncio.coroutine
    def device_type_read_handler(self, request):
        try:
            device_type = self.get_device_type(request)
        except ResponseError as ex:
            return ex.response

        manager = getattr(self.app, self.device_types[device_type]['manager'])

        return web.Response(text=json.dumps({'devices': list(manager.items.keys())}),
                            content_type='application/json',
                            status=200)

    @asyncio.coroutine
    def device_read_handler(self, request):
        try:
            device_type = self.get_device_type(request)
        except ResponseError as ex:
            return ex.response

        error_prefix = self.device_types[device_type]

        device_name = request.match_info['name']

        try:
            device = self.get_device(device_type=device_type, device_name=device_name,
                                     error_prefix=error_prefix)
        except ResponseError as ex:
            return ex.response

        return web.Response(text=json.dumps(device.get_structure()),
                            content_type='application/json',
                            status=200)

    @asyncio.coroutine
    def read_var_handler(self, request):
        try:
            device_type = self.get_device_type(request)
        except ResponseError as ex:
            return ex.response

        error_prefix = self.device_types[device_type]

        device_name = request.match_info['name']

        try:
            device = self.get_device(device_type=device_type, device_name=device_name,
                                     error_prefix=error_prefix)
        except ResponseError as ex:
            return ex.response

        var_name = request.match_info['varname']
        try:
            value = getattr(device, var_name)

            if callable(value):
                raise AttributeError()
        except AttributeError:
            return self.error_not_found_attribute(device_type=device_type,
                                                  error_prefix=error_prefix,
                                                  device_name=device_name,
                                                  var_name=var_name)

        return web.Response(text=json.dumps({var_name: value}),
                            content_type='application/json',
                            status=200)

    @asyncio.coroutine
    def write_var_handler(self, request):
        try:
            device_type = self.get_device_type(request)
        except ResponseError as ex:
            return ex.response

        error_prefix = self.device_types[device_type]

        device_name = request.match_info['name']

        try:
            device = self.get_device(device_type=device_type, device_name=device_name,
                                     error_prefix=error_prefix)
        except ResponseError as ex:
            return ex.response

        var_name = request.match_info['var_name']

        try:
            body = yield from request.json()
            value = body[var_name]
        except:
            return self.error_response(error_msg="Invalid body",
                                       error_code="00102",
                                       status=400)

        try:
            attr = getattr(device, var_name)

            if callable(attr):
                raise AttributeError()

        except AttributeError:
            return self.error_not_found_attribute(device_type=device_type,
                                                  error_prefix=error_prefix,
                                                  device_name=device_name,
                                                  var_name=var_name)

        setattr(device, var_name, value)
        return web.Response(text=json.dumps({var_name: value}),
                            content_type='application/json',
                            status=200)

    @asyncio.coroutine
    def call_handler(self, request):
        try:
            device_type = self.get_device_type(request)
        except ResponseError as ex:
            return ex.response

        error_prefix = self.device_types[device_type]

        device_name = request.match_info['name']

        try:
            device = self.get_device(device_type=device_type, device_name=device_name,
                                     error_prefix=error_prefix)
        except ResponseError as ex:
            return ex.response

        var_name = request.match_info['var_name']

        try:
            body = yield from request.json()
        except:
            return self.error_response(error_msg="Invalid body",
                                       error_code="00102",
                                       status=400)

        try:
            func = getattr(device, var_name)

            if not callable(func):
                raise AttributeError()

        except AttributeError:
            return self.error_not_found_attribute(device_type=device_type,
                                                  error_prefix=error_prefix,
                                                  device_name=device_name,
                                                  var_name=var_name)

        result = func(**body)
        return web.Response(text=json.dumps({var_name: result}),
                            content_type='application/json',
                            status=200)

    @asyncio.coroutine
    def start(self):
        yield from asyncio.get_event_loop().create_server(self.server.make_handler(),
                                                          self.config.get('host', "0.0.0.0"),
                                                          self.config.get('port', 8080))


def factory(app):
    return EnvSenseWebApplication(app)
