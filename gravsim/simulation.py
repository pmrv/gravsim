from math import fabs
from time import sleep
from copy import deepcopy
from itertools import permutations
from decimal import Decimal
from gravsim.vec2d import vec2d, linear_combination

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

        #return (self.gconst * mass1 * mass2 / radius ** 2)
        return 0

    def step (self):
        self.time += self.stepsize

        for thing, other in permutations (self.things, 2):

            # gravitational force
            grav_dir = (other.position - thing.position)
            grav_dir_norm = grav_dir.normalized ()
            grav_force = grav_dir * self.get_grav_force (
                    other.mass, thing.mass, grav_dir.length)
            thing.accelerate (id (other), grav_force/thing.mass)
            other.accelerate (id (thing), -grav_force/other.mass)

            # whether two things collide
            future_thing = deepcopy (thing)
            future_other = deepcopy (other)
            future_thing.move (self.stepsize)
            future_other.move (self.stepsize)
            vec_dist = abs (future_other.position - future_thing.position)
            if vec_dist.length - thing.radius - other.radius <= 0: # things collide
                sleep (.1)
                vec_dist_norm = vec_dist.normalized ()
                tangente_norm = vec_dist_norm.perpendicular_normal ()

                alpha1, beta1 = linear_combination (thing.velocity, tangente_norm, vec_dist_norm)
                alpha2, beta2 = linear_combination (other.velocity, tangente_norm, vec_dist_norm)

                thing.velocity = vec_dist_norm * beta2 + tangente_norm * alpha1
                other.velocity = vec_dist_norm * beta1 + tangente_norm * alpha2

        for thing in self.things:
            thing.move (self.stepsize)
