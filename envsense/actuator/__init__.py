import asyncio
from envsense.devices import BaseDeviceManager


class ActuatorDeviceManager(BaseDeviceManager):

    CONFIG_KEY = 'actuators'

    def __init__(self,  app):
        super(ActuatorDeviceManager, self).__init__(app)
        # Add sensors
        from .upm import LedActuator, BuzzerActuator, DisplayActuator
        self.items['LedActuator'] = LedActuator(refresh=1)
        self.items['BuzzerActuator'] = BuzzerActuator(refresh=1)
        self.items['DisplayActuator'] = DisplayActuator(refresh=1)

    @asyncio.coroutine
    def start(self):
        for actuator in self.items.values():
            asyncio.async(actuator.start(), loop=asyncio.get_event_loop())


def factory(app):
    return ActuatorDeviceManager(app)


class BaseActuator:

    def __init__(self, refresh=1, *args, **kwargs):
        self.refresh = refresh

    @asyncio.coroutine
    def start(self):
        while True:
            self.do_writing()
            yield from asyncio.sleep(self.refresh)

    def do_writing(self):
        pass

    def get_structure(self):
        return {'properties': {'refresh': self.refresh}}
