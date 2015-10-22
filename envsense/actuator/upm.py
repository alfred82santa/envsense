import time

import pyupm_grove as grove
import pyupm_buzzer as buzzer
import pyupm_i2clcd as i2clcd

from envsense.actuator import BaseActuator


class LedActuator(BaseActuator):

    def __init__(self, refresh=1, port=4, *args, **kwargs):
        super(LedActuator, self).__init__(refresh=refresh, *args, **kwargs)
        self.upm_sensor = grove.GroveLed(port)

    def do_writing(self, status=false):
        # status false -> led off, true ->  led on
        if status == false:
            self.upm_sensor.off()
        else:
            self.upm_sensor.on()

class BuzzerActuator(BaseActuator):

    def __init__(self, refresh=1, port=5, *args, **kwargs):
        super(BuzzerActuator, self).__init__(refresh=refresh, *args, **kwargs)
        self.upm_sensor = buzzer.Buzzer(port)
        self.chords = [buzzer.DO, buzzer.RE, buzzer.MI, buzzer.FA,
          buzzer.SOL, buzzer.LA, buzzer.SI, buzzer.DO,
          buzzer.SI]

    def do_writing(self, music=self.chords, pause_notes=0.1):
        # Play music notes pausing for 0.1 seconds between notes
        for chord_ind in range (0,len(music)):
            # play each note for one second
            print(buzzer.playSound(self.chords[chord_ind], 1000000))
            time.sleep(pause_notes)


class DisplayActuator(BaseActuator):

    def __init__(self, refresh=1, lcd_address=0x3E, rgb_address=0x62, *args, **kwargs):
        super(DisplayActuator, self).__init__(refresh=refresh, *args, **kwargs)
        self.upm_sensor = i2clcd.Jhd1313m1(0, lcd_address, rgb_address)


    def do_writing(self, color=(0,0), position=(255,0,0), text="Hello"):
        self.upm_sensor.setColor(*color)
        self.upm_sensor.setPosition(*position)
        self.upm.write(text)
        time.sleep(1000000)







