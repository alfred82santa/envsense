import asyncio
from envsense.manager import BaseManager


class ActuatorManager(BaseManager):

    CONFIG_KEY = 'actuators'

    def __init__(self,  app):
        super(ActuatorManager, self).__init__(app)
        # Add sensors
        # self.items['name'] = Actuator(refresh=1)

    @asyncio.coroutine
    def start(self):
        for actuator in self.items.values():
            asyncio.async(actuator.start(), loop=asyncio.get_event_loop())


def factory(app):
    return ActuatorManager(app)


class BaseActuator:

    def __init__(self, refresh=1, *args, **kwargs):
        self.refresh = refresh

    @asyncio.coroutine
    def start(self):
        self.do_writing()
        yield from asyncio.sleep(self.refresh)

    def do_writing(self):
        pass
