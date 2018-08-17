import asyncio
import logging

from . import common

logger = logging.getLogger('lutetium.meter')

class PVSim(common.LutetiumCommon):

    async def on_event(self, channel, body, envelope, properties):
        logger.info(body)
        await channel.basic_client_ack(envelope.delivery_tag)

    async def run(self):
        await self.connect()

        while True:
            await self.consume(self.on_event)
