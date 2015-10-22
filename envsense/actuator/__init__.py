import asyncio


class ActuatorManager:

    def __init__(self,  app):
        pass

@asyncio.coroutine
def factory(app):
    mng = ActuatorManager(app)
    yield from mng.start_actuators()
    return mng
