import asyncio
import importlib
import logging
from aiohttp import web
import aiohttp_jinja2
import jinja2
from generic import routes


class BaseCommandServer(object):

    def __init__(self, server_type=None, host=None, port=None, loop=None):
        logging.info('Init %s Server on host %s:%s' % (server_type, host, port))
        self._server_type = server_type
        self._loop = loop or asyncio.get_event_loop()
        self._init_server(host, port)

    def start(self):
        self._server = self._loop.run_until_complete(self._server)
        logging.info(' %s has started.' % (self._server_type))

    def stop(self):
        self._server.close()
        logging.info('%s has stopped.' % (self._server_type))

    def discover(self, module):
        globals()[module] = importlib.import_module(module)
        self._load_routes()


class HttpCommandServer(BaseCommandServer):
    _instance = None

    def _init_server(self, host, port):
        self._app = web.Application()
        self._load_routes()
        self._server = self._loop.create_server(self._app.make_handler(),
                                                host, port)

    def __init__(self, templates=None, **kwargs):
        super().__init__(**kwargs)
        if templates:
            aiohttp_jinja2.setup(self._app,
                                 loader=jinja2.FileSystemLoader(templates))

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(HttpCommandServer, cls).__new__(cls)
        return cls._instance

    def _load_routes(self):
        logging.debug('Loading  Application Routes:\n%s' % '\n'.join(str(r) for r in routes.ROUTES))
        for route in routes.ROUTES:
            self._app.router.add_route(*route)