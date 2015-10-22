import asyncio
import yaml


class EnvSenseApp:

    def __init__(self, config_file_path=None):
        self.sensor_manager = None
        self.actuator_manager = None
        self.web_app = None
        self.logic_manager = None

        if config_file_path:
            try:
                with open(config_file_path, 'r') as stream:
                    self.config = yaml.load(stream)
            except Exception as ex:
                print(ex)
                raise
        else:
            self.config = {}

        self.load_modules()

    def load_modules(self):
        self.sensor_manager = self.create_sensor_manager()
        self.actuator_manager = self.create_actuator_manager()
        self.logic_manager = self.create_logic_manager()
        self.web_app = self.create_web_app()

    def create_sensor_manager(self):
        from .sensor import factory
        return factory(self)

    def create_actuator_manager(self):
        from .actuator import factory
        return factory(self)

    def create_web_app(self):
        from .web import factory
        return factory(self)

    def create_logic_manager(self):
        from .logic import factory
        return factory(self)

    def start(self, loop=None):
        if loop is None:
            loop = asyncio.get_event_loop()

        if self.sensor_manager:
            asyncio.async(self.sensor_manager.start(), loop=loop)

        if self.actuator_manager:
            asyncio.async(self.actuator_manager.start(), loop=loop)

        if self.web_app:
            asyncio.async(self.web_app.start(), loop=loop)

        if self.logic_manager:
            asyncio.async(self.logic_manager.start(), loop=loop)

        asyncio.get_event_loop().run_forever()
