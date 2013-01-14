from gravsim.vec2d import vec2d

class Simulation (object):
    """
    This class represents the running simulation
    works on objects which have collide, move, accelerate methods
    and position and velocity parameters
    """

    def __init__(self, things, fieldsize, stepsize = .1):
        """
        Constructor.
        
        things -- objects to simulate
        fieldsize -- two-tuple, size of the world
        stepsize -- time in seconds which shall be simulated in one step
        """

        self.things = things
        self.fieldsize = fieldsize
        self.g = vec2d (0, 9.81)
        self.stepsize = stepsize

        for thing in self.things: thing.accelerate ("g", self.g)

        #things [0].accelerate ('a', vec2d (0, -11))

        self.xwall = vec2d (fieldsize [0], 0)
        self.ywall = vec2d (0, fieldsize [1])

        self.time = 0

    def step (self):

        for thing in self.things:
            self.time += self.stepsize
            thing.move (self.stepsize)

            trad = thing.radius

            if (self.ywall + (thing [0], -trad)) [1] < thing [1]:
                thing.mirror_velocity (1)
                thing [1] = self.ywall [1] - thing.radius - 1

            elif thing [1] - trad < 1:
                thing.mirror_velocity (1)
                thing [1] = 0 + thing.radius + 1

            if (self.xwall + (-trad, thing [1])) [0] < thing [0]:
                thing.mirror_velocity (0)
                thing [0] = self.xwall [0] - thing.radius - 1

            elif thing [0] - trad < 1:
                thing.mirror_velocity (0)
                thing [0] = 0 + thing.radius + 1

            if self.time % 1:
                print (thing.position, thing.velocity)
