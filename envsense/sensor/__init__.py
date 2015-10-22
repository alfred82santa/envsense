import asyncio


class SensorManager:

    def __init__(self,  app):
        pass


@asyncio.coroutine
def factory(app):
    mng = SensorManager(app)
    yield from mng.start()
    return mng
