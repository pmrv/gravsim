import gen_client
import argparse
from decimal import Decimal
from time import time

class FastCLI:

    argparser = argparse.ArgumentParser (add_help = False)

    def init (self, sim, args):
        self.start = time ()

    def step (self, sim):
        if sim.time < 1e3:
            return

        diff = time () - self.start

        print ("Sim time: {}".format (sim.time))
        print ("Real time: {}".format (diff))
        print ("Sim time per real time: {}".format (sim.time / Decimal ("{}".format (diff))))

        for t in sim.things:
            print (t.name)
            print ('\t', t.position, t.velocity)

        print ("Deviation in momentum: {}".format (sim.delta_impulse.length), sim.delta_impulse)

        return "quit"

fcli = FastCLI ()
gen_client.run ([fcli])
