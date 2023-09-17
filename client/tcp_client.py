import asyncio
import sys

class SubscriberClientProtocol(asyncio.Protocol):
    def __init__(self, loop, rcv_callback):
        self.transport = None
        self.loop = loop
        self.queue = asyncio.Queue()
        self._ready = asyncio.Event()
        self.rcv_callback = rcv_callback
        asyncio.ensure_future(self._send_messages())

    async def _send_messages(self):
        """ Send messages to the server as they become available. """
        await self._ready.wait()
        while True:
            data = await self.queue.get()
            self.transport.write(data.encode('utf-8'))
            print('Message sent: {!r}'.format(data))

    def connection_made(self, transport):
        """ Upon connection send the message to the server
        """
        self.transport = transport
        print("Connection made.")
        self._ready.set()

    async def send_message(self, data):
        """ Feed a message to the sender coroutine. """
        await self.queue.put(data)

    def data_received(self, data):
        self.rcv_callback(data)

    def connection_lost(self, exc):
        print('The server closed the connection')
        print('Stop the event loop')
        self.loop.stop()

class tcp_client():
    def __init__(self, host : str, port : int, rcv_callback):
        self.is_connected = False
        loop = asyncio.get_event_loop()

        self.protocol = asyncio.StreamReaderProtocol(asyncio.StreamReader())
        loop.connect_read_pipe(lambda: self.protocol, sys.stdin)

        try:
            coro = loop.create_connection(lambda: SubscriberClientProtocol(loop, rcv_callback), host, port)
            _, self.proto = loop.run_until_complete(coro)
            self.is_connected = True
        except ConnectionRefusedError as exp:
            print(exp.strerror)

    async def _send_messages(self, msg):
        await self.proto.send_message(msg)

    def send_messages(self, msg):
        if not self.is_connected:
            return "client is not connected"

        asyncio.ensure_future(self._send_messages(msg=msg))

        return None
