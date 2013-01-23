from math import fabs
from time import sleep
from copy import deepcopy
from itertools import permutations
from decimal import Decimal
from gravsim.vec2d import vec2d

class Simulation (object):
    """
    This class represents the running simulation
    works on objects which have collide, move, accelerate methods
    and position and velocity parameters
    """

    def __init__(self, things, stepsize = .1):
        """
        Constructor.
        
        things -- objects to simulate
        stepsize -- time in seconds which shall be simulated in one step
        """

        self.things   = things
        self.stepsize = stepsize
        self.gconst   = Decimal ('6.67384e-11')
        self.time     = 0

    def get_grav_force (self, mass1, mass2, radius):

        return (self.gconst * mass1 * mass2 / radius ** 2)

    def step (self):
        self.time += self.stepsize

        for thing, other in permutations (self.things, 2):

            grav_dir = (other.position - thing.position)
            grav_dir_norm = grav_dir.normalized ()
            grav_force = grav_dir * self.get_grav_force (
                    other.mass, thing.mass, grav_dir.length)
            thing.accelerate (id (other), grav_force/thing.mass)
            other.accelerate (id (thing), -grav_force/other.mass)

            future_thing = deepcopy (thing)
            future_other = deepcopy (other)
            future_thing.move (self.stepsize)
            future_other.move (self.stepsize)
            vec_dist = abs (future_other.position - future_thing.position)
            if vec_dist.length - thing.radius - other.radius <= 0: # things collide
                sleep (.1)
                horizontal = vec_dist.perpendicular_normal ()
                thing.velocity.rotate (-1 * 2 * horizontal.get_angle_between (thing.velocity))
                other.velocity.rotate (-1 * 2 * horizontal.get_angle_between (other.velocity))

        for thing in self.things:
            thing.move (self.stepsize)
