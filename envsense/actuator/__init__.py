import asyncio
from envsense.manager import BaseManager


class ActuatorManager(BaseManager):

    def __init__(self,  app):
        super(ActuatorManager, self).__init__(app)
        # Add sensors
        # self.items['name'] = Actuator(refresh=1)

    @asyncio.coroutine
    def start(self):
        for actuator in self.items.values():
            yield from actuator.start()


@asyncio.coroutine
def factory(app):
    mng = ActuatorManager(app)
    yield from mng.start()
    return mng


class BaseActuator:

    def __init__(self, refresh=1, *args, **kwargs):
        self.refresh = refresh

    @asyncio.coroutine
    def start(self):
        self.do_writing()
        yield from asyncio.sleep(self.refresh)

    def do_writing(self):
        pass
