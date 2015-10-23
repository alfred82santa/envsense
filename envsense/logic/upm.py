from envsense.logic import BaseLogic

class GasLogic(BaseLogic):

    def __init__(self, *args, **kwargs):
        super(GasLogic, self).__init__(*args, **kwargs)
        self.threshold = 70

    def do_process(self):
        if self.app.sensor_manager.items['GasSensor'].value > self.threshold:
            self.app.logic_manager.items['AlertLogic'].set_alert('GasLogic', 'alert', 'GAS ALERT: v='+ self.app.sensor_manager.items['GasSensor'].value, True)
        else:
            self.app.logic_manager.items['AlertLogic'].set_alert('GasLogic', 'information', 'GAS INFO: v='+ self.app.sensor_manager.items['GasSensor'].value, False)


class SoundLogic(BaseLogic):

    def __init__(self, *args, **kwargs):
        super(SoundLogic, self).__init__(*args, **kwargs)
        self.threshold = 70

    def do_process(self):
        if self.app.sensor_manager.items['SoundSensor'].value > self.threshold:
            self.app.logic_manager.items['AlertLogic'].set_alert('SoundSensor', 'alert', 'SOUND ALERT: v='+ self.app.sensor_manager.items['SoundSensor'].value, False)
        else:
            self.app.logic_manager.items['AlertLogic'].set_alert('SoundSensor', 'information', 'SOUND INFO: v='+ self.app.sensor_manager.items['SoundSensor'].value, False)


class UVLogic(BaseLogic):

    def __init__(self, *args, **kwargs):
        super(UVLogic, self).__init__(*args, **kwargs)
        self.threshold_low = 0.5
        self.threshold_high = 0.7

    def do_process(self):
        if self.app.sensor_manager.items['UVLogic'].value > self.threshold_high:
            self.app.logic_manager.items['AlertLogic'].set_alert('UVSensor', 'alert', 'UV ALERT: v='+ self.app.sensor_manager.items['UVSensor'].value, True)
        elif self.app.sensor_manager.items['UVLogic'].value > self.threshold_low:
            self.app.logic_manager.items['AlertLogic'].set_alert('UVSensor', 'warning', 'UV WARN: v='+ self.app.sensor_manager.items['UVSensor'].value, False)
        else:
            self.app.logic_manager.items['AlertLogic'].set_alert('UVSensor', 'information', 'UV INFO: v='+ self.app.sensor_manager.items['UVSensor'].value, False)


class LightLogic(BaseLogic):

    def __init__(self, *args, **kwargs):
        super(LightLogic, self).__init__(*args, **kwargs)
        self.threshold = 15

    def do_process(self):
        if self.app.sensor_manager.items['LightLogic'].value < self.threshold:
            self.app.logic_manager.items['AlertLogic'].set_alert('LightSensor', 'warning', 'Light WARN: v='+ self.app.sensor_manager.items['LightLogic'].value, False)
        else:
            self.app.logic_manager.items['AlertLogic'].set_alert('LightSensor', 'information', 'Light INFO: v='+ self.app.sensor_manager.items['LightLogic'].value, False)


class TempLogic(BaseLogic):

    def __init__(self, *args, **kwargs):
        super(TempLogic, self).__init__(*args, **kwargs)
        self.threshold_low1 = 0
        self.threshold_low2 = -10
        self.threshold_high1 = 30
        self.threshold_high2 = 35

    def do_process(self):
        if self.app.sensor_manager.items['TempLogic'].value > self.threshold_high2:
            self.app.logic_manager.items['AlertLogic'].set_alert('TempSensor', 'alert', 'TEMP ALERT: v='+ self.app.sensor_manager.items['TempSensor'].value, True)
        elif self.app.sensor_manager.items['TemperatureLogic'].value > self.threshold_high1:
            self.app.logic_manager.items['AlertLogic'].set_alert('TempSensor', 'warning', 'TEMP WARN: v='+ self.app.sensor_manager.items['TempSensor'].value, False)
        elif self.app.sensor_manager.items['TemperatureLogic'].value < self.threshold_low2:
            self.app.logic_manager.items['AlertLogic'].set_alert('TempSensor', 'alert', 'TEMP ALERT: v='+ self.app.sensor_manager.items['TempSensor'].value, True)
        elif self.app.sensor_manager.items['TemperatureLogic'].value < self.threshold_low1:
            self.app.logic_manager.items['AlertLogic'].set_alert('TempSensor', 'warning', 'TEMP WARN: v='+ self.app.sensor_manager.items['TempSensor'].value, False)
        else:
            self.app.logic_manager.items['AlertLogic'].set_alert('TempSensor', 'information', 'TEMP INFO: v='+ self.app.sensor_manager.items['TempSensor'].value, False)

class TouchLogic(BaseLogic):

    def __init__(self, *args, **kwargs):
        super(TouchLogic, self).__init__(*args, **kwargs)

    def do_process(self):
        if self.app.sensor_manager.items['TouchLogic'].value:
            self.app.logic_manager.items['AlertLogic'].remove_alert('TouchSensor')
