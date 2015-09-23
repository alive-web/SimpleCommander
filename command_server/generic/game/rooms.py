import uuid
from generic.game.base import GameFactory

OPENED_ROOMS = {}

"""
Room as entry point of server communication between clients
"""
class Room(object):

    def __init__(self, id, game_slug):
        self.id = id
        self.game = GameFactory(game_slug)()
        OPENED_ROOMS[id] = self

    @classmethod
    def start_new(cls, game_slug):
        return cls(str(uuid.uuid4()), game_slug)