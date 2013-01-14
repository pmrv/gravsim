import pygame
from pygame.locals import *
from math import ceil

from gravsim.things import Ball
from gravsim.simulation import Simulation

HEIGHT = 400
WIDTH  = 400
RAD    =  10

WHITE  = Color (200, 200, 200)
BLACK  = Color (000, 000, 000)

CLOCK = pygame.time.Clock ()
DISPLAY = pygame.display.set_mode ((HEIGHT, WIDTH))

balls = ( Ball (RAD, (200, 200), (0, 0)), )
#Ball (RAD, (100, 100), (0, 0)))
sim = Simulation (balls, (HEIGHT, WIDTH), .0001)

while True:

    DISPLAY.fill (WHITE)
    sim.step ()
    
    for b in sim.things:
        pygame.draw.circle (DISPLAY, BLACK, 
                (ceil (b [0]), ceil (b [1])), b.radius)

    pygame.display.update ()
    CLOCK.tick (60)

