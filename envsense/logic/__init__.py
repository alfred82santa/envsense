import asyncio
import weakref
from envsense.manager import BaseManager


class LogicManager(BaseManager):

    CONFIG_KEY = 'logics'

    def __init__(self,  app):
        super(LogicManager, self).__init__(app)
        # Add sensors
        # self.items['name'] = Logic(app, refresh=1)

    @asyncio.coroutine
    def start(self):
        for logic in self.items.values():
            asyncio.async(logic.start(), loop=asyncio.get_event_loop())


def factory(app):
    return LogicManager(app)


class BaseLogic:

    def __init__(self, app, refresh=1, *args, **kwargs):
        self.refresh = refresh
        self._app = weakref.ref(app)

    @property
    def app(self):
        return self._app()

    @asyncio.coroutine
    def start(self):
        self.do_process()
        yield from asyncio.sleep(self.refresh)

    def do_process(self):
        pass


class AlertLightLogic(BaseLogic):

    def do_process(self):
        if self.app.sensor_manager.items['light'].value > 100:
            self.app.actuator_manager.items['lcd'].set_alert('pepito')
