from time import time

import gen_client

class CLISim (object):

    def __init__ (self):
        pass

    def init (self, sim):

        self.timings = []
        self.old_time = 0
        self.old_simtime = 0

    def step (self, sim):

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
        new_simtime = sim.time
        self.mean_time = float (new_simtime - self.old_simtime) / (new_time - self.old_time)
        self.old_time = new_time
        self.old_simtime = new_simtime

        print ('\033[1;1H\033[J') # clear screen
        print ("dt = %f, time = %f, speed = %f" % (sim.stepsize, sim.time, self.mean_time))

        for t in sim.things:
            a = sum (t.a.values ())
            print (
        """
        %s\t@ (%f, %f):
        \tVelocity:\t%f (%08.8f, %08.8f)
        \tAcceleration:\t%f (%08.8f, %08.8f)
        """ % (t.name, t.position [0], t.position [1], t.velocity.length, t.velocity [0], t.velocity [1], a.length, a [0], a [1]) 
        )

        print ("\tForces:")
        for k, v in sim.grav_forces.items ():
            print ("\t%s <-> %s: %04f (%04f, %f)" % (k [0].name, k [1].name, v.length, v [0], v [1]))

        print ("\nImpulse deviation:")
        print ("\tThis step:   ", sim.step_delta_impulse)
        print ("\tSince start: ", sim.delta_impulse)

if __name__ == "__main__":
    module = CLISim ()
    gen_client.run ([module])
