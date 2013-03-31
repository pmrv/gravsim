from time import time

import gen_client

class CLISim (object):

    def __init__ (self):
        pass

    def init (self, sim):

        self.display_intervall = int (10 * sim.stepsize) if sim.stepsize >= .1 else 1
        self.last_print = 0
        self.timings = []

    def step (self, sim):

        if not sim.time % self.display_intervall:
            self.print_stats (sim)

    def get_time (self):
        return sum (self.timings) / len (self.timings)

    def set_time (self, print_time):
        self.timings.append (print_time)
        if len (self.timings) > 100: self.timings.pop (0)
    # wooho
    mean_time = property (get_time, set_time)

    def print_stats (self, sim):

        new_time = time ()
        self.mean_time = self.display_intervall / (new_time - self.last_print)
        self.last_print = new_time

        print ('\033[1;1H\033[J') # clear screen
        print ("dt = %f, time = %f, speed = %f" % (sim.stepsize, sim.time, self.mean_time))

        for t in sim.things:
            a = sum (t.a.values ())
            print (
        """
        %s\t@ (%f, %f):
        \tVelocity:\t(%08.8f, %08.8f)
        \tAcceleration:\t(%08.8f, %08.8f)
        """ % (t.name, t.position [0], t.position [1], t.velocity [0], t.velocity [1], a [0], a [1]) 
        )

        print ("\tForces:")
        for k, v in sim.grav_forces.items ():
            print ("\t%s <-> %s: %04f (%04f, %f)" % (k [0].name, k [1].name, v.length, v [0], v [1]))

if __name__ == "__main__":
    module = CLISim ()
    gen_client.run ([module])
