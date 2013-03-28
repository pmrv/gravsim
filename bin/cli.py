from time import time

import gen_client

class CLISim (object):

    def __init__ (self):
        pass

    def init (self, sim):

        self.display_intervall = int (10 * sim.stepsize) if sim.stepsize >= .1 else 1
        self.last_print = time ()

    def step (self, sim):

        if not sim.time % self.display_intervall:
            self.print_stats (sim)

    def print_stats (self, sim):

        new_time = time ()
        print ('\033[1;1H\033[J') # clear screen
        print ("dt = %f, time = %f, speed = %f" % (sim.stepsize, sim.time, self.display_intervall / (new_time - self.last_print)))
        self.last_print = new_time

        for t in sim.things:
            a = sum (t.a.values ())
            print (
        """
        %s\t@(%f, %f):
        \tVelocity:\t(%08.8f, %08.8f)
        \tAcceleration:\t(%08.8f, %08.8f)
        """ % (t.name, t.position [0], t.position [1], t.velocity [0], t.velocity [1], a [0], a [1]) 
        )

        print ("\tForces:")
        for k, v in sim.grav_forces.items ():
            print ("\t%s <-> %s: %04f (%04f, %f)" % (k [0].name, k [1].name, v.length, v [0], v [1]))


module = CLISim ()
gen_client.run (module)
