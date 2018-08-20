import json
import asyncio
import aioamqp
import logging

logger = logging.getLogger('lutetium.common')

class LutetiumCommon:
    publish_queue = None
    consume_queue = None

    def __init__(self, **kwargs):
        self.transport = None
        self.protocol = None
        self.channel = None
        self.amqp_config = kwargs.get('amqp_config', {})

    async def connect(self):
        tries = 0
        while True:
            try:
                self.transport, self.protocol = await aioamqp.connect(
                    **self.amqp_config
                )
            except:
                if tries > 10:
                    raise
                tries += 1

                logging.exception('Connection error, retrying (try #%s)', tries)

                # exponential backoff
                await asyncio.sleep(2 ** tries)
            else:
                break

        self.channel = await self.protocol.channel()

        for name in [self.publish_queue, self.consume_queue]:
            if name:
                await self.channel.queue_declare(queue_name=name)

    async def publish(self, message):
        if not isinstance(message, bytes):
            message = json.dumps(message).encode()

        return await self.channel.publish(message, '', self.publish_queue)

    async def consume(self, callback, queue=None):
        return await self.channel.basic_consume(callback, self.consume_queue)

    async def run(self):
        pass
