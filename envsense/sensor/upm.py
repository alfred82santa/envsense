import pyupm_grove as grove
from envsense.sensor import BaseSensor


class LightSensor(BaseSensor):

    def __init__(self, refresh=1, port=0, *args, **kwargs):
        super(LightSensor, self).__init__(refresh=refresh, *args, **kwargs)
        self.upm_sensor = grove.GroveLight(port)

    def do_reading(self):
        return self.upm_sensor.raw_value()
