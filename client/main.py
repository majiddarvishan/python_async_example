#!/usr/bin/env python3

from tcp_client import tcp_client

import asyncio
import json

# async def connect_stdin_stdout():
#     loop = asyncio.get_event_loop()
#     return reader

if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    clnt = tcp_client('127.0.0.1', 10666, lambda data : print('Message received: {!r}'.format(data.decode())))

    message = json.dumps({'type': 'subscribe', 'channel': 'sensor'}, separators=(',', ':'))

    clnt.send_messages(message)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print('Closing connection')
    loop.close()