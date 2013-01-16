from math import fabs
from time import sleep
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

        things [0].accelerate ('a', vec2d (0, -11))

        x1wall = (vec2d (0, 0), vec2d (fieldsize [0], 0))
        x2wall = (vec2d (0, fieldsize [1]), vec2d (fieldsize [0], 0))
        y1wall = (vec2d (0, 0), vec2d (0, fieldsize [1]))
        y2wall = (vec2d (fieldsize [0], 0), vec2d (0, fieldsize [1]))
        diagon = (vec2d (0, 0), vec2d (fieldsize))

        self.walls = (x1wall, x2wall, y1wall, y2wall, diagon)

    def step (self):

        for thing in self.things:
            self.time += self.stepsize
            thing.move (self.stepsize)

            trad = thing.radius

            for premise, border in self.walls:

                radius_vector = trad * border.perpendicular_normal ()
                
                present_angle = border.get_angle_between (thing.position - premise + radius_vector)
                future_angle = border.get_angle_between (
                        thing.position + thing.velocity * self.stepsize / 2 - premise - radius_vector
                )
                sign_p = present_angle / fabs (present_angle) if present_angle != 0 else 1
                sign_f = future_angle / fabs (future_angle) if future_angle != 0 else -1 * sign_p
                if sign_p != sign_f or present_angle == 0:
                    v_angle = border.get_angle_between (thing.velocity)
                    thing.velocity.rotate (-1 * 2 * v_angle)
