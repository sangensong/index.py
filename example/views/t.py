from indexpy.http import HTTPView
from indexpy.test import TestView
from indexpy.http import finished_response


@finished_response
def onlytest():
    _ = ...


class HTTP(HTTPView):
    async def get(self):
        onlytest()
        a = "temporary"
        raise Exception("SomeError.")
