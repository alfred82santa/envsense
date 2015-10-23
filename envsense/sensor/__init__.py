import asyncio

from envsense.devices import BaseDeviceManager, BaseDevice


class SensorDeviceManager(BaseDeviceManager):

    CONFIG_KEY = 'sensors'

    def __init__(self,  app):
        super(SensorDeviceManager, self).__init__(app)
        # Add sensors
        from .upm import LightSensor, TempSensor, UVSensor, TouchSensor, SoundSensor, GasSensor
        self.items['LightSensor'] = LightSensor(refresh=1)
        self.items['TempSensor'] = TempSensor(refresh=1)
        self.items['UVSensor'] = UVSensor(refresh=1)
        self.items['TouchSensor'] = TouchSensor(refresh=0.1)
        self.items['SoundSensor'] = SoundSensor(refresh=1)
        self.items['GasSensor'] = GasSensor(refresh=1)

    @asyncio.coroutine
    def start(self):
        for sensor in self.items.values():
            asyncio.async(sensor.start(), loop=asyncio.get_event_loop())


def factory(app):
    return SensorDeviceManager(app)


class BaseSensor(BaseDevice):

    def __init__(self, refresh=1, *args, **kwargs):
        self.refresh = refresh
        self.value = None

    @asyncio.coroutine
    def start(self):
        while True:
            self.value = self.do_reading()
            yield from asyncio.sleep(self.refresh)

    def do_reading(self):
        pass

    def get_structure(self):
        return {'properties': {'refresh': self.refresh},
                'readOnlyProperties': {'value': self.value}}




