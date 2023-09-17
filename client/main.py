from tcp_client import tcp_client

import asyncio
import json
import sys

async def feed_messages(protocol):
    """ An example function that sends the same message repeatedly. """
    message = json.dumps({'type': 'subscribe', 'channel': 'sensor'},
                         separators=(',', ':'))
    while True:
        await protocol.send_message(message)
        await asyncio.sleep(1)

# async def connect_stdin_stdout():
#     loop = asyncio.get_event_loop()
#     return reader

if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    clnt = tcp_client()

    message = json.dumps({'type': 'subscribe', 'channel': 'sensor'},
                            separators=(',', ':'))

    clnt.send_messages(message)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print('Closing connection')
    loop.close()