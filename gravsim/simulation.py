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

        self.old_impulse = sum (t.mass * t.velocity for t in self.things)

    def get_grav_force (self, mass1, mass2, radius):

        return (self.gconst * mass1 * mass2 / radius ** 2)
    
    def check_impulse (self):

        new_impulse = sum (t.mass * t.velocity for t in self.things)
        delta_imp = new_impulse - self.old_impulse
        self.old_impulse = new_impulse

        if delta_imp:
            raise Exception ("Impulse is off by {}".format (delta_imp))

    def step (self):
        self.time += self.stepsize

        for thing, other in permutations (self.things, 2):

            # gravitational force
            grav_dir = (other.position - thing.position)
            grav_dir_norm = grav_dir.normalized ()
            grav_force = grav_dir * self.get_grav_force (other.mass, thing.mass, grav_dir.length)
            thing.accelerate (other.name, grav_force/thing.mass)
            other.accelerate (thing.name, -grav_force/other.mass)

            # whether two things collide
            future_thing = deepcopy (thing)
            future_other = deepcopy (other)
            future_thing.move (self.stepsize)
            future_other.move (self.stepsize)
            vec_dist = future_other.position - future_thing.position
            if vec_dist.length - thing.radius - other.radius < 0: # things collide
                vec_dist_norm = vec_dist.normalized ()
                tangente_norm = vec_dist_norm.perpendicular_normal ()

                old_thing_velocity = thing.velocity
                old_other_velocity = other.velocity

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

