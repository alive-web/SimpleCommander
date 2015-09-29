import asyncio
from generic.game.signals import Signal


class BaseUnit(object):
    name = 'Unit'
    speed_period = 300 #miliseconds needs to update state
    state_class = UnitState

    def __init__(self, game):
        """
        :param game: BaseGame
        """
        self._game = game
        self._loop = game.loop or asyncio.get_event_loop()
        self._timer = self._loop.call_later(self.speed_period/1000, self._digest)

    def __hash__(self):
        return '{}-{}'.format(self.name, id(self))

    def _digest(self):
        self.digest()
        self.state.push()
        self._timer = self._loop.call_later(self.speed_period/1000, self._digest)

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

    @property
    def time(self):
        return self._game.time

    @property
    def state(self):
        return self.state_class(self)

    @state.setter
    def state(self, new_state):
        for attr, value in new_state.iteritem():
            setattr(self, attr, value)


class UnitState(dict):
    """
    All changes with units should be touched theirs state. It is as list of attributes that changes over time.
    State should be serializable, for sending it to client and store as game log.
    Serializable view:
    {
        _time: <timestamp in milliseconds>,
        attr1: value1,
        ...
        attrN: valueN,
    }
    """
    attributes = ()

    def __init__(self, unit, **kwargs):
        super().__init__(**kwargs)
        self.unit = unit
        self.time = unit.time

    def __iter__(self):
        for attr in self.attributes:
            if hasattr(self.unit, attr):
                yield attr
        yield '_time'

    def __getitem__(self, item):
        return getattr(self.unit, item, None) if item != '_time' else self.time

    def push(self):
        self.unit._game.push(self)

    @classmethod
    def create_from_dict(cls, state_dict):
        unit = object()
        unit._game = object()
        unit._game.time = state_dict.pop('_time')
        unit.__dict__ = state_dict
        return cls(unit)


class Position2D(object):
    __slots__ = ['x', 'y']

    def __init__(self, x=0, y=0):
        self.x, self.y = x, y

    def __iter__(self):
        yield self.x
        yield self.y

    def __add__(self, other):
        self.x += other[0]
        self.y += other[1]


class Position3D(object):
    __slots__ = ['x', 'y', 'z']

    def __init__(self, x=0, y=0, z=0):
        self.x, self.y, self.z = x, y, z

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z

    def __add__(self, other):
        self.x += other[0]
        self.y += other[1]


class Positioned2DMixin(object):
    position = Position2D(x=0, y=0)


class Positioned3DMixin(object):
    position = Position3D(x=0, y=0)


class Unit2D(Positioned2DMixin, BaseUnit):
    pass


class Unit3D(Positioned3DMixin, BaseUnit):
    pass