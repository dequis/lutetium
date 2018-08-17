import asyncio
import logging

from . import common

logger = logging.getLogger('lutetium.meter')

class Meter(common.LutetiumCommon):
    def __init__(self, meter_source, **kwargs):
        super().__init__(**kwargs)
        self.source = meter_source

    async def run(self):
        await self.connect()

        while True:
            message = self.source.step()
            await self.publish(message)
            await asyncio.sleep(1)
