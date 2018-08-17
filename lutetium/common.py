import json
import asyncio
import aioamqp
import logging

class LutetiumCommon:
    def __init__(self):
        self.transport = None
        self.protocol = None
        self.channel = None
        self.queue_name = 'lutetium'

    async def connect(self):
        self.transport, self.protocol = await aioamqp.connect()
        self.channel = await self.protocol.channel()
        await self.channel.queue_declare(queue_name=self.queue_name)

    async def publish(self, message):
        if not isinstance(message, bytes):
            message = json.dumps(message).encode()

        return await self.channel.publish(message, '', self.queue_name)

    async def consume(self, callback, queue=None):
        return await self.channel.basic_consume(callback, self.queue_name)

    async def run(self):
        pass
