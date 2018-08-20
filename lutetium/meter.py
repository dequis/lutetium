import asyncio
import logging

from . import common, protocol

logger = logging.getLogger('lutetium.meter')

class Meter(common.LutetiumCommon):
    def __init__(self, meter_source, **kwargs):
        super().__init__(**kwargs)
        self.source = meter_source
        self.seq = 0

    async def run(self):
        await self.connect()

        while True:
            self.seq += 1
            message = protocol.MeterMessage.make(
                seq=self.seq,
                value=self.source.step(),
            )

            logger.debug(message.decode())

            await self.publish(message)
            await asyncio.sleep(1)
