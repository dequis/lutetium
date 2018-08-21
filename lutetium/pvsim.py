import asyncio
import logging

from . import common, protocol

logger = logging.getLogger('lutetium.pvsim')

class PVSim(common.LutetiumCommon):
    consume_queue = 'lutetium_meter'
    publish_queue = 'lutetium_pvsim'

    def __init__(self, pvsim_source=None, **kwargs):
        super().__init__(**kwargs)
        self.source = pvsim_source
        self.seq = 0

    async def on_event(self, channel, body, envelope, properties):
        meter_message = protocol.MeterMessage().loads(body)

        self.seq += 1

        msg = {}
        msg['timestamp'] = meter_message['timestamp']
        msg['meter_value'] = meter_message['value']
        msg['pv_value'] = self.source.step(self.seq)
        msg['combined'] = msg['meter_value'] + msg['pv_value']
        msg['seq'] = self.seq

        pv_message = protocol.PVMessage.make(**msg)

        logger.debug(pv_message.decode())

        await self.publish(pv_message)

        await channel.basic_client_ack(envelope.delivery_tag)

    async def run(self):
        await self.connect()

        await self.consume(self.on_event)

        while self.seq < 1440:
            await asyncio.sleep(1)
