import asyncio
from generic.game import REGISTERED_GAMES
from generic.game.exeptions import GameAlreadyExists, GameNotExists


class game(type):
     def __new__(cls, name, bases, attrs):
        new_cls = type.__new__(cls, name, bases, attrs)
        if attrs.slug:
            if attrs.slug in REGISTERED_GAMES:
                raise GameAlreadyExists
            REGISTERED_GAMES[new_cls] = new_cls
        return new_cls


class BaseGame(metaclass=game):
    name = 'Game'
    version = '0.1.0'
    slug = None

    def __init__(self, loop):
        self.loop = loop or asyncio.get_event_loop()
        self.units = {}

    @classmethod
    def __hash__(cls):
        return '{}'.format(cls.__name__)

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


class GameFactory(object):

    def __init__(self, game_slug):
        self.game_slug = game_slug

    def __call__(self, *args, **kwargs):
        self.create(*args, **kwargs)

    def create(self, *args, **kwargs):
        if self.game_slug not in REGISTERED_GAMES:
            raise GameNotExists
        return REGISTERED_GAMES[self.game_slug](*args, **kwargs)
