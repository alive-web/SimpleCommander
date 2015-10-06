import asyncio
import configparser
import logging
from aiohttp import server

from generic.server import HttpCommandServer

DEBUG = True

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('etc/command_server.conf')
    host = config.get('commandServer', 'host')
    port = config.get('commandServer', 'port')
    templates = config.get('commandServer', 'templates')
    logging.basicConfig(level=logging.DEBUG)
    loop = asyncio.get_event_loop()
    server = HttpCommandServer(server_type='Http Server', host=host, port=port, loop=loop, templates=templates)
    server.discover('generic.game')
    try:
        server.start()
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.stop()
        loop.close()
