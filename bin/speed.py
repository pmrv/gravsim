import argparse
import time
import gravsim.view

class SpeedView (gravsim.view.View):

    argparser = argparse.ArgumentParser (add_help = None)
    argparser.add_argument ("-m", metavar = "MAX", 
            type = int,required = True,
            help = "Time to run in simulated seconds.",
            dest = "tmax")

    def __init__ (self):

        gravsim.view.View.__init__ (
            self, description = "Shows average simulated time per real time.")

    def run (self):
        before = time.time ()
        while self.sim.time < self.tmax:
            self.step (self.stepsize)

        print ( self.sim.time / (time.time () - before) )

if __name__ == "__main__":
    s = SpeedView ()
    s.run ()
