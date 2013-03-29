import sys, os, csv
from decimal import Decimal

from gravsim.things import Ball
from gravsim.simulation import Simulation

def init ():

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
    sim = Simulation (things, stepsize, verbose = True)
    return sim

def loop (sim, module):

    while True:
        sim.step ()
        module.step (sim)

def run (module):

    sim = init ()
    module.init (sim)
    loop (sim, module)
