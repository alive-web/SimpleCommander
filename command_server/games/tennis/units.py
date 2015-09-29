from generic.game import units


class BallState(units.UnitState):
    attributes = ('position',)


class Ball(units.Unit2D):
    name = 'Ball'
    state_class = BallState
    speed_period = 1000

    movement_vector = units.Vector2D(0, 1)

    def digest(self):
        self.position += self.movement_vector