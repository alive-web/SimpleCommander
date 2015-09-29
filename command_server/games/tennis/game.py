from generic.game.base import BaseGame
from games.tennis import units


class TennisGame(BaseGame):
    name = 'Tennis'
    version = '0.0.1'
    slug = 'tennis'

    def init(self):
        self.add_unit(units.Ball(self))
        self.start()