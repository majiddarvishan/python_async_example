#!/usr/bin/env python3

# https://stackoverflow.com/questions/64303607/python-asyncio-how-to-read-stdin-and-write-to-stdout

from tcp_client import tcp_client

import asyncio
import json
import sys

async def read_stdin():
    loop = asyncio.get_event_loop()
    reader = asyncio.StreamReader()
    protocol = asyncio.StreamReaderProtocol(reader)
    await loop.connect_read_pipe(lambda: protocol, sys.stdin)
    # w_transport, w_protocol = await loop.connect_write_pipe(asyncio.streams.FlowControlMixin, sys.stdout)
    # writer = asyncio.StreamWriter(w_transport, w_protocol, reader, loop)
    while True:
        res = await reader.read(100)
        if not res:
            break

        print(res)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    clnt = tcp_client('127.0.0.1', 10666, lambda data : print(f'Message received: {data}'))

    message = json.dumps({'type': 'subscribe', 'channel': 'sensor'}, separators=(',', ':'))

    clnt.send_messages(message)

    asyncio.ensure_future(read_stdin())

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print('Closing connection')
    loop.close()