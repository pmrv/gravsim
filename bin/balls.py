import pygame
from pygame.locals import *
from math import ceil

from gravball.gravball import Ball
from gravball.simulation import Simulation

HEIGHT = 400
WIDTH  = 400
RAD    =  10

WHITE  = Color (200, 200, 200)
BLACK  = Color (000, 000, 000)

CLOCK = pygame.time.Clock ()
DISPLAY = pygame.display.set_mode ((HEIGHT, WIDTH))

balls = ( Ball (RAD, (200, 200), (10, 0)), Ball (RAD, (100, 200), (-10, 0)))
sim = Simulation (balls, (HEIGHT, WIDTH))

while True:

    DISPLAY.fill (WHITE)
    sim.step (0.1)
    
    for b in sim.things:
        pygame.draw.circle (DISPLAY, BLACK, 
                (ceil (b [0]), ceil (b [1])), b.radius)

    pygame.display.update ()
    CLOCK.tick (60)

