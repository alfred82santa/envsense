import asyncio
from envsense.manager import BaseManager


class SensorManager(BaseManager):

    CONFIG_KEY = 'sensors'

    def __init__(self,  app):
        super(SensorManager, self).__init__(app)
        # Add sensors
        # self.items['name'] = Sensor(refresh=1)

    @asyncio.coroutine
    def start(self):
        for sensor in self.items.values():
            asyncio.async(sensor.start(), loop=asyncio.get_event_loop())


def factory(app):
    return SensorManager(app)


class BaseSensor:

    def __init__(self, refresh=1, *args, **kwargs):
        self.refresh = refresh
        self.value = None

    @asyncio.coroutine
    def start(self):
        self.value = self.do_reading()
        yield from asyncio.sleep(self.refresh)

    def do_reading(self):
        pass




