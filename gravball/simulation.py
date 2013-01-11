from gravball.vec2d import vec2d

class Simulation (object):
    """
    This class represents the running simulation
    works on objects which have collide and move methods
    and position and velocity parameters
    """

    def __init__(self, things, fieldsize, stepsize = 1):
        """
        Constructor.
        
        things -- objects to simulate
        fieldsize -- two-tuple, size of the world
        stepsize -- time in seconds which shall be simulated in one step
        """

        self.things = things
        self.fieldsize = fieldsize
        self.g = vec2d (0, 9.81)
        self.step = step

        # points which the Things are not supposed to move through
        self.bottom = [ (i, self.fieldsize [1] - 1)
                for i in range (self.fieldsize [1]) ]
        self.top    = [ (i, 0) for i in range (self.fieldsize [1]) ]
        self.left   = [ (0, i) for i in range (self.fieldsize [0]) ]
        self.right  = [ (self.fieldsize [0] - 1, i) 
                for i in range (self.fieldsize [0]) ]

    def step (self):

        for thing in self.things:
            thing.move (self.step)

            if thing.collide ( self.bottom [int (thing [0])] ):
                thing.mirror_velocity (1)
                thing [1] = self.fieldsize [1] - thing.radius
            elif thing.collide ( self.top [int (thing [0])] ):
                thing.mirror_velocity (1)
                thing [1] = 0 + thing.radius
            if thing.collide ( self.left [int (thing [1])] ):
                thing [0] = 0 + thing.radius
                thing.mirror_velocity (0)
            elif thing.collide ( self.right [int (thing [1])] ): 
                thing.mirror_velocity (0)
                thing [0] = self.fieldsize [0] - thing.radius

        for thing in self.things:
            thing.add_velocity (self.g * self.step) 
