"""
Each game should run scenario and can have many of them.
At least one scenario should be exists in a game.
e.g. ('Single player', 'Multi player', '1 vs PC', ...) etc.
"""
class Scenario(object):
    name = None
    description = None

    def __init__(self, game):
        self.game = game

    def start(self):
        self.game.start()