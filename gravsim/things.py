import math
from time import sleep
from decimal import Decimal
from gravsim.vec2d import vec2d

class Ball (object):

    def __init__ (self, name, radius, mass, position = (0, 0), velocity = (0, 0)):

        self.name = name
        self.position = vec2d (position)
        self.velocity = vec2d (velocity)
        self.a = {self: vec2d (0, 0)} # to prevent that sum (self.a) returns 0.0
        self.radius = Decimal (radius)
        self.mass = Decimal (mass)

    def move (self, t):
        a = sum (self.a.values ())
        self.position += (a / 2) * (t ** 2) + self.velocity * t
        self.velocity += a * t

    def accelerate (self, name, a):
        self.a [name] = a

    def __getitem__ (self, k):
        return self.position [k]

    def __setitem__ (self, k, v):
        self.position.__setitem__ (k, v)
