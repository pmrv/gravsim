import pygame
from pygame.locals import *
from math import ceil, sqrt
from time import sleep
from decimal import Decimal

from gravsim.vec2d import vec2d
from gravsim.things import Ball
from gravsim.simulation import Simulation

HEIGHT = Decimal (700)
WIDTH  = Decimal (700)
RAD    = Decimal ( 10)

WHITE  = Color (255, 255, 255)
BLACK  = Color (000, 000, 000)

CLOCK = pygame.time.Clock ()
DISPLAY = pygame.display.set_mode ((WIDTH, HEIGHT))

FACTOR = Decimal ("1")
DISPLAY_BORDER = 20 
#balls  = (Ball (RAD, 10000, (155, 190), (100, 100)), Ball (RAD, 100000, (45, 50), (170, 90)))#, Ball (RAD, 10, (50, 300), (0, -15)))
earth = Ball (6371000, 10e24, (0, 0), (0, 0))
moon = Ball (1737100, 10e21, (0, 20000000), (20220000, 0))
sim = Simulation ((earth, moon), .01)
max_display_length = Decimal (min (WIDTH, HEIGHT)) / 2

while True:

    DISPLAY.fill (WHITE)
    max_position = 0

    for b in sim.things:
        if b.position.length > max_position:
            max_position = b.position.length

        pygame.draw.circle (DISPLAY, BLACK, 
                (ceil (b [0] * FACTOR) + WIDTH / 2, ceil (b [1]) * FACTOR + HEIGHT / 2), b.radius * FACTOR)
    sim.step ()

    FACTOR = (max_display_length - DISPLAY_BORDER)  / max_position

    pygame.display.update ()
    CLOCK.tick (60)

