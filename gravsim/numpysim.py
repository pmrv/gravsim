from numpy import float64, array
from numpy.core.numeric import outer

G  = 6.67384e-11

def step (positions, accelerations, masses):
    diagind = tuple (range (0, len (accelerations)))
    accdiag = accelerations [ [diagind, diagind] ]
    mm = outer (masses, masses)
    dp = array ( [positions - positions [i] for i in range (len (positions))], dtype = float64 )
    r3 = (dp**2).sum (axis = -1) ** (3/2) * mm
    r3 = array ( [r3, r3] ).swapaxes (0, -1)
    accelerations [:,:,:] = G * dp / r3
    accelerations [ (diagind, diagind) ] = accdiag

def move (positions, velocities, accelerations, t):
    a = accelerations.sum (axis = 1)
    positions  += a / 2 * t ** 2 + velocities * t
    velocities += a * t
