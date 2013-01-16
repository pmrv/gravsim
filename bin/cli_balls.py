from time import sleep
from math import fabs
from gravsim.things import Ball
from gravsim.simulation import Simulation

ball = Ball (10, (200, 200))
sim = Simulation ((ball, ), (400,400)) 

while True:
    sim.step ()
