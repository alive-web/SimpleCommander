import asyncio
import time
from generic.game import REGISTERED_GAMES
from generic.game.exeptions import GameAlreadyExists, GameNotExists
from generic.game.signals import Signal


class game(type):
     def __new__(cls, name, bases, attrs):
        new_cls = type.__new__(cls, name, bases, attrs)
        if attrs['slug']:
            if attrs['slug'] in REGISTERED_GAMES:
                raise GameAlreadyExists
            REGISTERED_GAMES[attrs['slug']] = new_cls
        return new_cls


class BaseGame(metaclass=game):
    name = 'Game'
    version = '0.1.0'
    slug = None
    keep_alive_period = 5
    scenarios = ()

    @classmethod
    def info(cls, extended=False):
        info = {
            'name': cls.name,
            'version': cls.version,
            'slug': cls.slug,
        }
        if extended:
            extended_info = {
                'scenarios': cls.get_scenarios_info()
            }
            info.update(extended_info)
        return info

    @classmethod
    def get_scenarios_info(cls):
        return {s.name: s.description for s in cls.scenarios}

    def __init__(self, loop=None):
        self.loop = loop or asyncio.get_event_loop()
        self._transport = None
        self._delayed_start = False

        self.units = {}
        self.start_time = 0 #store game start in timestamp
        self.init()

    def init(self):
        pass

    def __repr__(self):
        return  '{} <{}>'.format(self.name, self.version)

    def add_unit(self, unit):
        self.units[unit] = unit

    def destroy_unit(self, unit):
        unit.destroy()
        del self.units[unit]

    def broadcast(self, signal):
        self.on(signal)

    def on(self, signal):
        for unit in self.units.values():
            unit.on(signal)

    @property
    def transport(self):
        return self._transport

    @transport.setter
    def transport(self, value):
        self._transport = value
        self._keep_alive_timer = self.loop.call_later(self.keep_alive_period, self.keep_alive)
        if self._delayed_start:
            self.start(delayed=False)

    def push(self, state):
        self.transport.send(state)

    def start(self, delayed=True):
        if self.transport:
            self.start_time = time.time() * 1000
            self.on(Signal('start'))
        elif delayed:
            self._delayed_start = True

    @property
    def time(self):
        return (time.time() * 1000) - self.start_time

    def keep_alive(self):
        self.transport.send(self.info())
        self._keep_alive_timer = self.loop.call_later(self.keep_alive_period, self.keep_alive)


class GameFactory(object):

    def __init__(self, game_slug):
        self.game_slug = game_slug

    def __call__(self, *args, **kwargs):
        return self.create(*args, **kwargs)

    def create(self, *args, **kwargs):
        if self.game_slug not in REGISTERED_GAMES:
            raise GameNotExists
        return REGISTERED_GAMES[self.game_slug](*args, **kwargs)
