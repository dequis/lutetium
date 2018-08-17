import asyncio
import logging

from . import common

logger = logging.getLogger('lutetium.pvsim')

class PVSim(common.LutetiumCommon):

    def __init__(self, pvsim_source=None, **kwargs):
        super().__init__(**kwargs)
        self.source = pvsim_source

    async def on_event(self, channel, body, envelope, properties):
        logger.info(body)
        await channel.basic_client_ack(envelope.delivery_tag)

    async def run(self):
        await self.connect()

        while True:
            await self.consume(self.on_event)
