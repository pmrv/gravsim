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
        self.time = 0

        for thing in self.things: thing.accelerate ("g", self.g)

        #things [0].accelerate ('a', vec2d (0, -11))

        self.xwall = vec2d (fieldsize [0], 0)
        self.ywall = vec2d (0, fieldsize [1])

    def step (self):

        for thing in self.things:
            self.time += self.stepsize

            trad = thing.radius

            for axis, wall in enumerate ( (self.ywall, self.xwall) ):

                other = (axis + 1) % 2
                if (wall + (thing [axis], -trad)) [other] < thing [other]:
                    thing.mirror_velocity (other)
                    thing [other] = wall [other] - thing.radius - 1
                    break

                # another generalization needed to get rid of this
                elif thing [other] - trad < 1:
                    thing.mirror_velocity (other)
                    thing [other] = 0 + thing.radius + 1
                    break
        else:
            thing.move (self.stepsize)

    def __repr__ (self):
        return self.position.__repr__ () + self.velocity.__repr__ ()

    __str__ = __repr__
