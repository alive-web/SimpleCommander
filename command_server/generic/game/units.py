import asyncio
from collections import namedtuple
from generic.game.signals import Signal

Position2D = namedtuple('Position2D', ['x', 'y'])
Position3D = namedtuple('Position3D', ['x', 'y', 'z'])


class BaseUnit(object):
    name = 'Unit'
    speed_period = 300 #miliseconds needs to update state
    state = UnitState

    def __init__(self, game):
        self._game = game
        self._loop = game.loop or asyncio.get_event_loop()
        self._timer = self._loop.call_later(self.speed_period/1000, self._digest)

    def __hash__(self):
        return '{}-{}'.format(self.name, id(self))

    def _digest(self):
        self.digest()
        self.state(self).push()
        self._timer = self._loop.call_later(self.speed_period/1000, self.digest)

    def digest(self):
        """
        Main method that will trigger periodically with own speed_period
        :return:
        """
        pass

    def destroy(self):
        self._timer.cancel()

    def broadcast_signal(self, signal):
        self._game.broadcast(signal)

    def broadcast(self, signal_name, *args, **kwargs):
        signal = Signal(signal_name, *args, **kwargs)
        self.broadcast_signal(signal)

    def on(self, signal):
        assert isinstance(signal, Signal), 'Bad signal type'
        method = getattr(self, 'on_{}'.format(signal.name))
        if method and callable(method):
            method(*signal.args, **signal.kwargs)


class UnitState(dict):
    """
    All changes with units should be touched theirs state. It is as list of attributes that changes over time.
    State should be serializable, for sending it to client and store as game log.
    """
    attributes = ()

    def __init__(self, unit, **kwargs):
        super().__init__(**kwargs)
        self.unit = unit
        self.time = unit._game.time
        unit.state = self

    def __iter__(self):
        return (attr for attr in self.attributes if hasattr(self.unit, attr))

    def __getitem__(self, item):
        return getattr(self.unit, item, None)

    def push(self):
        self.unit._game.push(self)

class Positioned2DMixin(object):
    position = Position2D(x=0, y=0)


class Positioned3DMixin(object):
    position = Position3D(x=0, y=0)


class Unit2D(Positioned2DMixin, BaseUnit):
    pass


class Unit3D(Positioned3DMixin, BaseUnit):
    pass