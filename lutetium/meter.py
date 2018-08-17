import asyncio
import logging

from . import common

logger = logging.getLogger('lutetium.meter')

class Meter(common.LutetiumCommon):

    async def run(self):
        await self.connect()

        while True:
            await self.publish(b'hello from meter')
            await asyncio.sleep(1)
