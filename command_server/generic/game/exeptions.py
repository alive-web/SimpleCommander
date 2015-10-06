class GameException(Exception):
    pass


class GameAlreadyExists(GameException):
    pass


class GameNotExists(GameException):
    pass