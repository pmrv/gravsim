import argparse
import gravsim.sim

class View:

    def __init__ (self, **kwargs):
        p = getattr (self, "argparser", None) # check whether subclasses defined their own args
        parser = argparse.ArgumentParser (parents = (p,) if p else [], **kwargs)

        parser.add_argument ("world", type = str, 
                help = "Path to world file.")
        parser.add_argument ("-t", type = float, metavar = "T",
                default = .1, required = False, dest = "stepsize",
                help = "Second which are simulated in one step.")
        #parser.add_argument ("-c", action = "store_true", dest = "collision",
        #        help = "Whether the simulation should account for collision between bodies.")
            
        args = parser.parse_args ()

        self.stepsize = args.stepsize
        self.sim = gravsim.sim.Sim (args.world)
