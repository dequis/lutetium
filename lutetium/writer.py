import logging

from . import common, protocol

logger = logging.getLogger('lutetium.writer')

class Writer(common.LutetiumCommon):
    consume_queue = 'lutetium_pvsim'

    def __init__(self, filename, **kwargs):
        super().__init__(**kwargs)
        self.file = open(filename, 'a')
        self.seq = 0

    async def on_event(self, channel, body, envelope, properties):
        pv_message = protocol.PVMessage().loads(body)

        self.file.write(body.decode() + '\n')
        self.file.flush()

        await channel.basic_client_ack(envelope.delivery_tag)

    async def run(self):
        await self.connect()

        await self.consume(self.on_event)
