import asyncio


class LogicManager:

    def __init__(self,  app):
        pass

@asyncio.coroutine
def factory(app):
    mng = LogicManager(app)
    yield from mng.start()
    return mng

