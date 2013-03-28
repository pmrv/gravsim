from math import fabs
from time import sleep
from copy import deepcopy
from itertools import combinations
from decimal import Decimal
from gravsim.vec2d import vec2d, linear_combination

class Simulation (object):
    """
    This class represents the running simulation
    works on objects which have collide, move, accelerate methods
    and position and velocity parameters
    """

    def __init__(self, things, stepsize = Decimal (".1"), verbose = False):
        """
        Constructor.
        
        things -- objects to simulate
        stepsize -- time in seconds which shall be simulated in one step
        """

        self.things   = things
        self.stepsize = stepsize
        self.gconst   = Decimal ('6.67384e-11')
        self.verbose  = verbose

        if self.verbose:
            self.time     = 0
            self.old_impulse = sum (t.mass * t.velocity for t in self.things)
            self.delta_impulse, self.step_delta_impulse = (0,0), (0,0)
            self.grav_forces = {}

    def get_grav_force (self, mass1, mass2, radius):

        return (self.gconst * mass1 * mass2 / radius ** 2)
    
    def check_impulse (self):

        new_impulse   = sum (t.mass * t.velocity for t in self.things)
        delta_impulse = new_impulse - self.old_impulse
        self.step_delta_impulse = self.delta_impulse - delta_impulse
        self.delta_impulse = delta_impulse

    def step (self):

        for thing, other in combinations (self.things, 2):

            # gravitational force
            grav_dir = (other.position - thing.position)
            grav_dir_norm = grav_dir.normalized ()
            grav_force = grav_dir_norm * self.get_grav_force (other.mass, thing.mass, grav_dir.length)
            thing.accelerate (other.name, grav_force/thing.mass)
            other.accelerate (thing.name, -grav_force/other.mass)
            if self.verbose: self.grav_forces [(thing, other)] = grav_force

            # whether two things collide
            future_thing = deepcopy (thing)
            future_other = deepcopy (other)
            future_thing.move (self.stepsize)
            future_other.move (self.stepsize)
            vec_dist = future_other.position - future_thing.position
            if vec_dist.length - thing.radius - other.radius < 0: # things collide
                vec_dist_norm = vec_dist.normalized ()
                tangente_norm = vec_dist_norm.perpendicular_normal ()

                alpha1, beta1 = linear_combination (thing.velocity, tangente_norm, vec_dist_norm)
                alpha2, beta2 = linear_combination (other.velocity, tangente_norm, vec_dist_norm)

                thing_collide_speed = beta1 * vec_dist_norm # speed component in the direction of other
                other_collide_speed = beta2 * vec_dist_norm 

                thing.velocity = (tangente_norm * alpha1 +
                        ((thing.mass - other.mass) * thing_collide_speed + 2 * other.mass * other_collide_speed) / (thing.mass + other.mass)
                )
                other.velocity = (tangente_norm * alpha2 + 
                        ((other.mass - thing.mass) * other_collide_speed + 2 * thing.mass * thing_collide_speed) / (thing.mass + other.mass)
                )


        for thing in self.things:
            thing.move (self.stepsize)

        if self.verbose:
            self.time += self.stepsize
            self.check_impulse ()

