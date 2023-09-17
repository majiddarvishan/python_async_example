import asyncio
import json
import sys

class SubscriberClientProtocol(asyncio.Protocol):
    def __init__(self, loop):
        self.transport = None
        self.loop = loop
        self.queue = asyncio.Queue()
        self._ready = asyncio.Event()
        asyncio.ensure_future(self._send_messages())

    async def _send_messages(self):
        """ Send messages to the server as they become available. """
        await self._ready.wait()
        while True:
            data = await self.queue.get()
            self.transport.write(data.encode('utf-8'))
            print('Message sent: {!r}'.format(data))

    def connection_made(self, transport):
        """ Upon connection send the message to the
        server

        A message has to have the following items:
            type:       subscribe/unsubscribe
            channel:    the name of the channel
        """
        self.transport = transport
        print("Connection made.")
        self._ready.set()

    async def send_message(self, data):
        """ Feed a message to the sender coroutine. """
        await self.queue.put(data)

    def data_received(self, data):
        """ After sending a message we expect a reply
        back from the server

        The return message consist of three fields:
            type:           subscribe/unsubscribe
            channel:        the name of the channel
            channel_count:  the amount of channels subscribed to
        """
        print('Message received: {!r}'.format(data.decode()))

    def connection_lost(self, exc):
        print('The server closed the connection')
        print('Stop the event loop')
        self.loop.stop()

class tcp_client():
    def __init__(self):
        loop = asyncio.get_event_loop()
        coro = loop.create_connection(lambda: SubscriberClientProtocol(loop), '127.0.0.1', 10666)

        # reader = asyncio.StreamReader()
        self.protocol = asyncio.StreamReaderProtocol(asyncio.StreamReader())
        loop.connect_read_pipe(lambda: self.protocol, sys.stdin)

        _, self.proto = loop.run_until_complete(coro)

    def send_messages(self, msg):
        asyncio.ensure_future(self._send_messages(msg=msg))

    async def _send_messages(self, msg):
        await self.proto.send_message(msg)
