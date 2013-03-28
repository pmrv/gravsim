import sys, os, csv
from time import time
from decimal import Decimal

from gravsim.simulation import Simulation
from gravsim.things import Ball


def print_stats (sim):

    global LAST_PRINT

    new_time = time ()
    print ('\033[1;1H\033[J') # clear screen
    print ("dt = %f, time = %f, speed = %f" % (sim.stepsize, sim.time, INTERVALL / (new_time - LAST_PRINT)))
    LAST_PRINT = new_time

    for t in sim.things:
        a = sum (t.a.values ())
        print (
    """
    %s\t@(%f, %f):
    \tVelocity:\t(%.8f, %.8f)
    \tAcceleration:\t(%.8f, %.8f)
    """ % (t.name, t.position [0], t.position [1], t.velocity [0], t.velocity [1], a [0], a [1]) 
    )

    print ("\tForces:")
    for k, v in sim.grav_forces.items ():
        print ("\t%s <-> %s: %f (%f, %f)" % (k [0].name, k [1].name, v.length, v [0], v [1]))


world_files = os.listdir ("worlds")
if len (world_files) == 0:
    print ("No worlds available.")
    sys.exit ()
if len (sys.argv) > 1 and sys.argv [1] in world_files:
    world = sys.argv [1]
else:
    world = world_files [0]

things = []
with open ("./worlds/" + world, 'r') as f:
    reader = csv.reader (f)
    for line in reader:
        if line [0].strip () [0] == '#': continue
        if len (line) < 7:
            raise Exception ('malformed line in csv')

        name    = line [0]
        radius  = Decimal (line [1])
        mass    = Decimal (line [2])
        pos     = line [3:5]
        vel     = line [5:7]

        things.append (Ball (name, radius, mass, pos, vel))

stepsize = Decimal (sys.argv [2]) if len (sys.argv) > 2 else Decimal (".1")
INTERVALL = int (10 * stepsize) if stepsize >= .1 else 1
LAST_PRINT = time ()

sim = Simulation (things, stepsize, verbose = True)

while True:

    sim.step ()
    if not sim.time % INTERVALL:
        print_stats (sim)

