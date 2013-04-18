import sys, os, csv, time
from decimal import Decimal
import argparse

from gravsim.things import Ball
from gravsim.simulation import Simulation

def parseworld (worldpath):

    things = []
    with open (worldpath, 'r') as f:
        reader = csv.reader (f)
        for line in reader:
            if line [0].strip () [0] == '#': continue
            if len (line) < 7:
                raise Exception ("Malformed line in world file.")

            name    = line [0]
            radius  = Decimal (line [1])
            mass    = Decimal (line [2])
            pos     = line [3:5]
            vel     = line [5:7]

            things.append (Ball (name, radius, mass, pos, vel))
    
    return things

def init (modules):

    parser = argparse.ArgumentParser (
            description = "Generalized client module to the gravsim simulation.",
            parents = [mod.argparser for mod in modules])

    parser.add_argument ("world", type = str, 
            help = "Name of world in the './worlds' directory.")
    parser.add_argument ("-t", type = float, metavar = "T",
            default = .1, required = False, dest = "stepsize",
            help = "Second which are simulated in one step.")
    parser.add_argument ("-v", action = "store_true", dest = "verbose",
            help = "Whether the simulation should collect additional information while running.")
    parser.add_argument ("-c", action = "store_true", dest = "collision",
            help = "Whether the simulation should account for collision between bodies.")

    args = parser.parse_args ()

    things = parseworld (os.path.join ("worlds", args.world))
    stepsize = Decimal ("%f" % args.stepsize) # fucking hate floats...
    sim = Simulation (things, stepsize, verbose = args.verbose, collision = args.collision)

    for module in modules: 
        module.init (sim, args)

    return sim

def loop (sim, modules):

    while True:
        sim.step ()
        for module in modules: 
            if module.step (sim) == "quit":
                sys.exit ()

def run (modules):

    if not modules: raise Exception ("No modules.")
    sim = init (modules)

    loop (sim, modules)
