import asyncio
import time
from generic.game import REGISTERED_GAMES
from generic.game.exeptions import GameAlreadyExists, GameNotExists


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

    @classmethod
    def info(cls):
        return {
            'name': cls.name,
            'version:': cls.version,
            'slug': cls.slug,
        }

    def __init__(self, loop=None):
        self.loop = loop or asyncio.get_event_loop()
        self.transport = None

        self.units = {}
        self.start_time = 0 #store game start in timestamp

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

    def push(self, state):
        self.transport.push(state)

    def start(self):
        self.start_time = time.time() * 1000

    @property
    def time(self):
        return (time.time() * 1000) - self.start_time


class GameFactory(object):

    def __init__(self, game_slug):
        self.game_slug = game_slug

    def __call__(self, *args, **kwargs):
        self.create(*args, **kwargs)

    def create(self, *args, **kwargs):
        if self.game_slug not in REGISTERED_GAMES:
            raise GameNotExists
        return REGISTERED_GAMES[self.game_slug](*args, **kwargs)
