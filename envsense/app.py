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

        self.load_modules()

    def load_modules(self):
        self.sensor_manager = asyncio.get_event_loop().run_until_complete(self.create_sensor_manager())
        self.actuator_manager = asyncio.get_event_loop().run_until_complete(self.create_actuator_manager())
        self.web_app = asyncio.get_event_loop().run_until_complete(self.create_web_app())
        self.logic_manager = asyncio.get_event_loop().run_until_complete(self.create_logic_manager())

    @asyncio.coroutine
    def create_sensor_manager(self):
        from .sensor import factory
        yield from factory(self)

    @asyncio.coroutine
    def create_actuator_manager(self):
        from .actuator import factory
        yield from factory(self)

    @asyncio.coroutine
    def create_web_app(self):
        from .web import factory
        yield from factory(self)

    @asyncio.coroutine
    def create_logic_manager(self):
        from .logic import factory
        yield from factory(self)

    def start(self):
        asyncio.get_event_loop().run_forever()
