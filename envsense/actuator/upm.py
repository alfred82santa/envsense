import time

import pyupm_grove as grove
import pyupm_buzzer as buzzer
import pyupm_i2clcd as i2clcd

from envsense.actuator import BaseActuator


class LedActuator(BaseActuator):

    def __init__(self, refresh=1, port=4, *args, **kwargs):
        super(LedActuator, self).__init__(refresh=refresh, *args, **kwargs)
        self.upm_sensor = grove.GroveLed(port)
        self.status = False

    def do_writing(self, status=False):
        # status false -> led off, true ->  led on
        if self.status:
            self.upm_sensor.on()
        else:
            self.upm_sensor.off()

    def get_structure(self):
        struct = super(LedActuator, self).get_structure()
        struct['properties']['status'] = self.status
        return struct


class BuzzerActuator(BaseActuator):

    def __init__(self, refresh=1, port=5, *args, **kwargs):
        super(BuzzerActuator, self).__init__(refresh=refresh, *args, **kwargs)
        self.upm_sensor = buzzer.Buzzer(port)
        self.chords = [buzzer.DO, buzzer.RE, buzzer.MI, buzzer.FA,
                       buzzer.SOL, buzzer.LA, buzzer.SI, buzzer.DO,
                       buzzer.SI]
        self.chord = None
        self.time = 1000000

    def do_writing(self):
        if self.chord:
            buzzer.playSound(self.chord, self.time)

    def get_structure(self):
        struct = super(LedActuator, self).get_structure()
        struct['properties']['chord'] = self.chord
        struct['properties']['time'] = self.time
        return struct


class DisplayActuator(BaseActuator):

    def __init__(self, refresh=1, lcd_address=0x3E, rgb_address=0x62, *args, **kwargs):
        super(DisplayActuator, self).__init__(refresh=refresh, *args, **kwargs)
        self.upm_sensor = i2clcd.Jhd1313m1(0, lcd_address, rgb_address)
        self.color = (255, 0, 0)
        self.cursor = (0, 0)
        self.text = "Hello"

    def do_writing(self):
        self.upm_sensor.setColor(*self.color)
        self.upm_sensor.setCursor(*self.cursor)
        self.upm.write(self.text)







