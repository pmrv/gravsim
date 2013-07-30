from numpy import float64, array, sqrt
from numpy.core.numeric import outer
from numpy.core.multiarray import zeros
from numpy.lib.npyio import loadtxt
from time import time
import csv


class Sim:

    G = 6.67384e-11

    def __init__ (self, worldfile):

        with open (worldfile) as world:
            reader = csv.reader (world)
            names = {}
            for k, line in enumerate (reader):
                names [line [0]] = k

        data = loadtxt (worldfile, delimiter = ',', usecols = range (1, 7), dtype = float64)
        self.names = names
        self.radii = data [:, 0]
        self.masses = data [:, 1]
        self.positions = data [:, 2:4]
        self.velocities = data [:, 4:]
        self.accelerations = zeros ( (len (self.names),) + self.positions.shape, dtype = float64)

        self.mm = outer (self.masses, self.masses)
        self.diagind = tuple (range (0, len (self.accelerations)))

        self.time = 0

    def step (self, t):

        self.time += t

        accdiag = self.accelerations [ (self.diagind, self.diagind) ]

        dp = array ( [self.positions - self.positions [i] for i in range (len (self.positions))], dtype = float64 )
        r3 = (dp**2).sum (axis = -1) ** (3/2) / self.mm
        r3 = array ( (r3, r3) ).swapaxes (0, -1)

        self.accelerations [:,:,:] = self.G * dp / r3
        self.accelerations [0] /= self.masses [0]
        self.accelerations [1] /= self.masses [1]
        self.accelerations [2] /= self.masses [2]
        self.accelerations [ (self.diagind, self.diagind) ] = accdiag

        a = self.accelerations.sum (axis = 1)
        self.positions  += a / 2 * t ** 2 + self.velocities * t
        self.velocities += a * t

