import time
import argparse
import gravsim.sim

class View:

    def __init__ (self, **kwargs):
        p = getattr (self, "argparser", None) # check whether subclasses defined their own args
        parser = argparse.ArgumentParser (parents = (p,) if p else [], **kwargs)

        parser.add_argument ("world", type = str, 
                help = "Path to world file.")
        parser.add_argument ("-t", type = float, metavar = "T",
                default = .1, dest = "stepsize",
                help = "Second which are simulated in one step.")
        parser.add_argument ("-f", type = int, 
                default = 20, dest = "fps",
                help = "How many times in a second the view code should run.")
            
        args = parser.parse_args ()
        self.__dict__.update (vars (args))

        self.sim = gravsim.sim.Sim (self.world)
        self.lastrun = 0
        self.lastsim = 0

    def step (self, deltasim):
        """
        deltasim  -- float, sim secs passed since the last call to this function
        """
        pass # overwriten by subclasses

    def run (self):
        try:
            while 1: 
                self.sim.step (self.stepsize)
                now = time.time ()
                deltareal = now - self.lastrun
                if deltareal > 1 / self.fps:
                    self.step (self.sim.time - self.lastsim)
                    self.lastsim = self.sim.time
                    self.lastrun = now
        except KeyboardInterrupt:
            print ("")
