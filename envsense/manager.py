import asyncio


class BaseManager:

    CONFIG_KEY = 'base'

    def __init__(self, app):
        self.items = {}
        self.app = app
        self.config = app.config.get(self.CONFIG_KEY)

    @asyncio.coroutine
    def init_manager(self):


