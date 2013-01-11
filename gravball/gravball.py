import math

from gravball.vec2d import vec2d

class Ball (object):

    def __init__ (self, radius, pos_or_pair = (0, 0), vec_or_pair = (0, 0)):

        self.position = vec2d (pos_or_pair)
        self.velocity = vec2d (vec_or_pair)
        self.radius = radius

    def collide (self, p):
        
        distance = math.sqrt (
            (self.position [0] - p [0])**2 + (self.position [1] - p [1]) ** 2)
        return distance < self.radius

    def move (self, t):
        # this doesn't seem to be quite right
        self.position += self.velocity / 2 * t + self.velocity * t

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

    def __getitem__ (self, k):
        return self.position [k]

    def __setitem__ (self, k, v):
        self.position.__setitem__ (k, v)
