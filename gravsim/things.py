import math
from time import sleep

from gravsim.vec2d import vec2d

class Ball (object):

    def __init__ (self, radius, mass, position = (0, 0), velocity = (0, 0)):

        self.position = vec2d (position)
        self.velocity = vec2d (velocity)
        self.a = {}
        self.radius = radius
        self.mass = mass

    def collide (self, p):
        
        distance = math.sqrt (
            (self.position [0] - p [0])**2 + (self.position [1] - p [1]) ** 2)
        return distance < self.radius

    def move (self, t):
        # this doesn't seem to be quite right
        a = sum (self.a.values ())
        self.position += (a / 2) * (t ** 2) + self.velocity * t
        self.velocity += a * t

    def mirror_velocity (self, k):
        """
        mirrors velocity along a given axis
        k = 1 X, 0 Y
        """
        self.velocity [k] *= -1

    def add_velocity (self, v):
        if not isinstance (v, vec2d):
            v = vec2d (v)

        self.velocity += v

    def accelerate (self, k, accel):
        self.a [k] = accel

    def __getitem__ (self, k):
        return self.position [k]

    def __setitem__ (self, k, v):
        self.position.__setitem__ (k, v)
