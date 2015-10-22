import asyncio
import json
import weakref
from aiohttp import web


class EnvSenseWebApplication:

    def __init__(self, app, *args, **kwargs):
        self._app = weakref.ref(app)
        self.server = web.Application(*args, **kwargs)
        self.server.router.add_route('GET', '/', self.default_handler)

    @property
    def app(self):
        return self._app()

    @asyncio.coroutine
    def default_handler(self, request):
        return web.Response(text=json.dumps({'hello': "world"}),
                            content_type='application/json',
                            status=200)


@asyncio.coroutine
def factory(app):
    webapp = EnvSenseWebApplication(app)
    server_config = app.config.get('server')
    yield from asyncio.get_event_loop().create_server(webapp.server.make_handler(),
                                                      server_config.get('host', "0.0.0.0"),
                                                      server_config.get('port', 8080))

    return webapp
