import asyncio
import weakref
from envsense.manager import BaseManager


class LogicManager(BaseManager):

    def __init__(self,  app):
        super(LogicManager, self).__init__(app)
        # Add sensors
        # self.items['name'] = Logic(app, refresh=1)

    @asyncio.coroutine
    def start(self):
        for logic in self.items.values():
            yield from logic.start()


@asyncio.coroutine
def factory(app):
    mng = LogicManager(app)
    yield from mng.start()
    return mng


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
