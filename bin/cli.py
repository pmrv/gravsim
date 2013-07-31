import time
import functools
import math
import gravsim.view

class CLIView (gravsim.view.View):

    def __init__ (self):

        gravsim.view.View.__init__ (self, description = "CLI View to the gravsim 'engine'.")

        self.timings = []
        self.display_time = 100
        self.firstimpulse = self.sim.get_allimpulse ()

    def step (self, deltasim):

        print ("\033[1;1H\033[J", end = "") # clear screen
        print ("time step: %f, sim time: %f, sim sec per real sec: %f" % (self.stepsize, self.sim.time, deltasim * self.fps // 1.))

        print ("====")

        heads = ["Name", "Radius", "Mass", "Distance", "Velocity", "Position"]
        for i, h in enumerate (heads):
            heads [i] = h.center (12 if i < 5 else 23)

        data = [heads]
        field  = functools.partial ( "{:^12,.5}".format )
        dfield = functools.partial ( "{:+11,.5},{:+11,.5}".format )
        for name, i in self.sim.names.items ():

            line = [
                    "{:^12}".format (name),
                    field  (self.sim.radii  [i]),
                    field  (self.sim.masses [i]),
                    field  (math.sqrt (sum (self.sim.positions  [i] ** 2)) ),
                    field  (math.sqrt (sum (self.sim.velocities [i] ** 2)) ),
                    dfield (*self.sim.positions [i]),
                   ]
            data.append (line)

        for line in data:
            print ("|".join (line))

        print ("====")
        print (self.firstimpulse, self.sim.get_allimpulse ())
        print ("impulse deviation since the beginning: %f" % ((self.firstimpulse - self.sim.get_allimpulse ()) / self.firstimpulse))

if __name__ == "__main__":
    view = CLIView ()
    view.run ()
