from time import sleep
from math import fabs
from gravsim.things import Ball
from gravsim.simulation import Simulation

ball = Ball (10, (200, 200))
sim = Simulation ((ball, ), (400,400)) 
oldvs = 1

while True:
    sim.step ()

    v = ball.velocity [1]
    vs = v / fabs (v)
    if vs != oldvs:
        print (ball.position, ball.velocity)
        sleep (.5)
    oldvs = vs
