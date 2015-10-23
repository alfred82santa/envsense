import pyupm_grove as grove
import pyupm_guvas12d as guvas12d
import pyupm_ttp223 as ttp223
import pyupm_mic as mic
import pyupm_gas as gas

from envsense.sensor import BaseSensor


class LightSensor(BaseSensor):

    def __init__(self, refresh=1, port=0, *args, **kwargs):
        super(LightSensor, self).__init__(refresh=refresh, *args, **kwargs)
        self.upm_sensor = grove.GroveLight(port)

    def do_reading(self):
        # aprox value of lux
        return self.upm_sensor.value()


class TempSensor(BaseSensor):

    def __init__(self, refresh=1, port=2, *args, **kwargs):
        super(TempSensor, self).__init__(refresh=refresh, *args, **kwargs)
        self.upm_sensor = grove.GroveTemp(port)

    def do_reading(self):
        # Celsius
        return self.upm_sensor.value()


class UVSensor(BaseSensor):

    def __init__(self, refresh=1, port=3, aref=5.0, samples=1024, *args, **kwargs):
        super(UVSensor, self).__init__(refresh=refresh, *args, **kwargs)
        self.upm_sensor = guvas12d.GUVAS12D(port)
        self.aref = aref
        self.samples = samples

    def do_reading(self):
        # Celsius
        return self.upm_sensor.value(self.aref, self.samples)

    def get_structure(self):
        struct = super(UVSensor, self).get_structure()
        struct['properties']['aref'] = self.aref
        struct['properties']['samples'] = self.samples
        return struct


class TouchSensor(BaseSensor):

    def __init__(self, refresh=1, port=2, *args, **kwargs):
        super(TouchSensor, self).__init__(refresh=refresh, *args, **kwargs)
        self.upm_sensor = ttp223.TTP223(port)

    def do_reading(self):
        # true or false
        return self.upm_sensor.isPressed()


class SoundSensor(BaseSensor):

    def __init__(self, refresh=1, port=3, averageReading=0, runningAverage=0, averagedOver=2,  *args, **kwargs):
        super(SoundSensor, self).__init__(refresh=refresh, *args, **kwargs)
        self.upm_sensor = mic.Microphone(port)
        self.threshContext = mic.thresholdContext()
        self.threshContext.averageReading = averageReading
        self.threshContext.runningAverage = runningAverage
        self.threshContext.averagedOver = averagedOver
        self.buffer = mic.uint16Array(128)

    def do_reading(self):
        length = self.upm_sensor.getSampledWindow(2, 128, self.buffer);
        if length > 0:
            return self.upm_sensor.findThreshold(self.threshContext, 30, self.buffer, length)
        else:
            return 0

    @property
    def average_reading(self):
        return self.threshContext.averageReading

    @average_reading.setter
    def set_average_reading(self, value):
        self.threshContext.averageReading = value

    @property
    def running_average(self):
        return self.threshContext.runningAverage

    @running_average.setter
    def set_running_average(self, value):
        self.threshContext.runningAverage = value

    @property
    def averaged_over(self):
        return self.threshContext.averagedOver

    @averaged_over.setter
    def set_average_reading(self, value):
        self.threshContext.averagedOver = value

    def get_structure(self):
        struct = super(SoundSensor, self).get_structure()
        struct['properties']['averageReading'] = self.threshContext.averageReading
        struct['properties']['runningAverage'] = self.threshContext.runningAverage
        struct['properties']['averagedOver'] = self.threshContext.averagedOver
        return struct


class GasSensor(BaseSensor):

    def __init__(self, refresh=1, port=1, averageReading=0, runningAverage=0, averagedOver=2,  *args, **kwargs):
        super(GasSensor, self).__init__(refresh=refresh, *args, **kwargs)
        self.upm_sensor = gas.MQ5(port)
        self.threshContext = gas.thresholdContext()
        self.threshContext.averageReading = averageReading
        self.threshContext.runningAverage = runningAverage
        self.threshContext.averagedOver = averagedOver
        self.buffer = gas.uint16Array(128)

    @property
    def average_reading(self):
        return self.threshContext.averageReading

    @average_reading.setter
    def set_average_reading(self, value):
        self.threshContext.averageReading = value

    @property
    def running_average(self):
        return self.threshContext.runningAverage

    @running_average.setter
    def set_running_average(self, value):
        self.threshContext.runningAverage = value

    @property
    def averaged_over(self):
        return self.threshContext.averagedOver

    @averaged_over.setter
    def set_average_reading(self, value):
        self.threshContext.averagedOver = value

    def do_reading(self):
        length = self.upm_sensor.getSampledWindow(2, 128, self.buffer)
        if length > 0:
            return self.upm_sensor.findThreshold(self.threshContext, 30, self.buffer, length)
        else:
            return 0
