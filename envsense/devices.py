import asyncio
import weakref


class BaseDeviceManager:

    CONFIG_KEY = 'base'

    def __init__(self, app):
        self.items = {}
        self._app = weakref.ref(app)
        self.config = app.config.get(self.CONFIG_KEY, {})

    @property
    def app(self):
        return self._app()

    @asyncio.coroutine
    def start(self):
        pass


class BaseDevice:

    def get_structure(self):
        return {'properties': {}, 'readOnlyProperties': {}, 'functions': {}}
