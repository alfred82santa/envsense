import asyncio
import weakref


class BaseManager:

    CONFIG_KEY = 'base'

    def __init__(self, app):
        self.items = {}
        self._app = weakref.ref(app)
        self.config = app.config.get(self.CONFIG_KEY)

    @property
    def app(self):
        return self._app()

    @asyncio.coroutine
    def init_manager(self):
        pass


