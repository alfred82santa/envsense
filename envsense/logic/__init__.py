import asyncio
import weakref
from collections import OrderedDict
from envsense.devices import BaseDeviceManager, BaseDevice


class LogicDeviceManager(BaseDeviceManager):

    CONFIG_KEY = 'logics'

    def __init__(self,  app):
        super(LogicDeviceManager, self).__init__(app)
        # Add sensors
        self.items['AlertLogic'] = AlertLogic(app, refresh=0.1)
        self.items['BuzzerAlertLogic'] = BuzzerAlertLogic(app, refresh=0.5)
        self.items['LedAlertLogic'] = LedAlertLogic(app, refresh=0.5)

        from .upm import GasLogic, SoundLogic, UVLogic, LightLogic, TempLogic, TouchLogic
        self.items['GasLogic'] = GasLogic(app, refresh=0.5)
        self.items['SoundLogic'] = SoundLogic(app, refresh=0.5)
        self.items['UVLogic'] = UVLogic(app, refresh=0.5)
        self.items['LightLogic'] = LightLogic(app, refresh=0.5)
        self.items['TempLogic'] = TempLogic(app, refresh=0.5)
        self.items['TouchLogic'] = TouchLogic(app, refresh=0.1)

    @asyncio.coroutine
    def start(self):
        for logic in self.items.values():
            asyncio.async(logic.start(), loop=asyncio.get_event_loop())


def factory(app):
    return LogicDeviceManager(app)


class BaseLogic(BaseDevice):

    def __init__(self, app, refresh=1, *args, **kwargs):
        self.refresh = refresh
        self._app = weakref.ref(app)

    @property
    def app(self):
        return self._app()

    @asyncio.coroutine
    def start(self):
        while True:
            yield from self.do_process()
            yield from asyncio.sleep(self.refresh)

    @asyncio.coroutine
    def do_process(self):
        pass


class BuzzerAlertLogic(BaseLogic):

    def __init__(self, *args, **kwargs):
        super(BuzzerAlertLogic, self).__init__(*args, **kwargs)
        self.active = False
        self.time = 3

    @asyncio.coroutine
    def do_process(self):
        actuator = self.app.actuator_manager.items['BuzzerActuator']
        import pyupm_buzzer as buzzer
        if self.active:
            actuator.chord = buzzer.DO
        else:
            actuator.chord = None


class LedAlertLogic(BaseLogic):

    def __init__(self, *args, **kwargs):
        super(LedAlertLogic, self).__init__(*args, **kwargs)
        self.active = False

    @asyncio.coroutine
    def do_process(self):
        led_green = self.app.actuator_manager.items['GreenLedActuator']
        led_red = self.app.actuator_manager.items['RedLedActuator']
        if self.active:
            led_green.status = False
        else:
            led_green.status = True

        led_red.status = not led_green.status


class AlertLogic(BaseLogic):

    ALERT = 'alert'
    WARN = 'warning'
    INFO = 'information'

    def __init__(self, *args, **kwargs):
        super(AlertLogic, self).__init__(*args, **kwargs)
        self.alerts = OrderedDict()
        self.stop_buffer = False

    def set_alert(self, device_name, level, text, buzzer=False):
        if device_name in self.alerts and level == self.ALERT and self.alerts[device_name]['level'] != self.ALERT:
            self.stop_buffer = False
        self.alerts[device_name] = {'level': level, 'text': text, 'buzzer': buzzer}

    def remove_alert(self, device_name):
        del self.alerts[device_name]

    @asyncio.coroutine
    def do_process(self):
        alerts = [alrt for alrt in self.alerts.values() if alrt['level'] == self.ALERT]
        warns = [alrt for alrt in self.alerts.values() if alrt['level'] == self.WARN]
        infos = [alrt for alrt in self.alerts.values() if alrt['level'] == self.INFO]

        actuator = self.app.actuator_manager.items['DisplayActuator']

        if len(alerts):
            actuator.color = (255, 0, 0)
            alrt = alerts[0]
            actuator.line_1 = alrt['text']
            if len([a for a in alerts if a['buzzer']]) and not self.stop_buffer:
                self.app.logic_manager.items['BuzzerAlertLogic'].active = True


            self.app.logic_manager.items['LedAlertLogic'].active = True

        elif len(warns):
            actuator.color = (255, 255, 0)
            alrt = warns[0]
            actuator.line_1 = alrt['text']
            self.app.logic_manager.items['LedAlertLogic'].active = True
            self.app.logic_manager.items['BuzzerAlertLogic'].active = False
        else:
            actuator.color = (0, 255, 0)
            if len(infos):
                alrt = infos[0]
                actuator.line_1 = alrt['text']
            self.app.logic_manager.items['LedAlertLogic'].active = False
            self.app.logic_manager.items['BuzzerAlertLogic'].active = False

        actuator.line_2 = "A:{};W:{};I:{}".format(len(alerts), len(warns), len(infos))

    def get_structure(self):
        struct = super(AlertLogic, self).get_structure()
        struct['functions']['set_alert'] = {'device_name': 'string',
                                            'level': [self.ALERT, self.WARN, self.INFO],
                                            'text': 'string',
                                            'buzzer': 'bool'}
        struct['functions']['remove_alert'] = {'device_name': 'string'}
        return struct
