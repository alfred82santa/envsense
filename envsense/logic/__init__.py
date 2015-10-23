import asyncio
import weakref
from envsense.devices import BaseDeviceManager, BaseDevice


class LogicDeviceManager(BaseDeviceManager):

    CONFIG_KEY = 'logics'

    def __init__(self,  app):
        super(LogicDeviceManager, self).__init__(app)
        # Add sensors
        # self.items['name'] = Logic(app, refresh=1)

    @asyncio.coroutine
    def start(self):
        for logic in self.items.values():
            asyncio.async(logic.start(), loop=asyncio.get_event_loop())


def factory(app):
    return LogicDeviceManager(app)


class BaseLogic(BaseDevice):

    def __init__(self, app, refresh=1, *args, **kwargs):
        self.refresh = refresh
        self._app = weakref.ref(app)

    @property
    def app(self):
        return self._app()

    @asyncio.coroutine
    def start(self):
        while True:
            yield from self.do_process()
            yield from asyncio.sleep(self.refresh)

    @asyncio.coroutine
    def do_process(self):
        pass


class AlertLightLogic(BaseLogic):

    def do_process(self):
        if self.app.sensor_manager.items['light'].value > 100:
            self.app.actuator_manager.items['lcd'].set_alert('pepito')
