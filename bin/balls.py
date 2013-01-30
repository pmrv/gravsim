import pygame
from pygame.locals import *
from math import ceil
from time import sleep
from decimal import Decimal

from gravsim.vec2d import vec2d
from gravsim.things import Ball
from gravsim.simulation import Simulation

HEIGHT = 700
WIDTH  = 700
RAD    =  10

WHITE  = Color (255, 255, 255)
BLACK  = Color (000, 000, 000)

CLOCK = pygame.time.Clock ()
DISPLAY = pygame.display.set_mode ((WIDTH, HEIGHT))

FACTOR = Decimal ("1")
balls  = (Ball (RAD, 10, (50, 190), (0, 0)), Ball (RAD, 10, (50, 50), (0, 30)))
#earth = Ball (6371000, 10e24, (40000000, 40000000), (0, 0))
#moon = Ball (1737100, 10e21, (40000000, 20000000), (20220000, 0))
sim = Simulation (balls, .01)

while True:

    DISPLAY.fill (WHITE)

    for b in sim.things:
        print (b.position)
        pygame.draw.circle (DISPLAY, BLACK, 
                (ceil (b [0] * FACTOR), ceil (b [1]) * FACTOR), b.radius * FACTOR)
    sim.step ()

    pygame.display.update ()
    CLOCK.tick (60)

