import asyncio
from envsense.manager import BaseManager


class SensorManager(BaseManager):

    def __init__(self,  app):
        super(SensorManager, self).__init__(app)
        # Add sensors
        # self.items['name'] = Sensor(refresh=1)

    @asyncio.coroutine
    def start(self):
        for sensor in self.items.values():
            yield from sensor.start()


@asyncio.coroutine
def factory(app):
    mng = SensorManager(app)
    yield from mng.start()
    return mng


class BaseSensor:

    def __init__(self, refresh=1, *args, **kwargs):
        self.refresh = refresh

    @asyncio.coroutine
    def start(self):
        self.do_reading()
        yield from asyncio.sleep(self.refresh)

    def do_reading(self):
        pass

