import asyncio
import logging
import datetime

from . import common, protocol

logger = logging.getLogger('lutetium.meter')

class Meter(common.LutetiumCommon):
    publish_queue = 'lutetium_meter'

    def __init__(self, meter_source, **kwargs):
        super().__init__(**kwargs)
        self.source = meter_source
        self.seq = 0

    async def run(self):
        await self.connect()

        while True:
            self.seq += 1

            timestamp = datetime.datetime.combine(
                datetime.date.today(),
                datetime.time.min,
            ) + datetime.timedelta(
                minutes=self.seq
            )

            message = protocol.MeterMessage.make(
                seq=self.seq,
                timestamp=timestamp,
                value=self.source.step(self.seq),
            )

            logger.debug(message.decode())

            await self.publish(message)
            await asyncio.sleep(1)
