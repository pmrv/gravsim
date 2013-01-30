import pygame, sys
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
DISPLAY = pygame.display.set_mode ((WIDTH, HEIGHT), RESIZABLE)

FACTOR = Decimal ("1")
DISPLAY_BORDER = 50 
MAX_DISPLAY_LENGTH = Decimal (min (WIDTH, HEIGHT)) / 2
balls  = (Ball (RAD, 100, (-50, 0), (40, 0)), Ball (RAD, 1, (20, 19), (-40, 0)))#, Ball (RAD, 10, (50, 300), (0, -15)))
earth = Ball (6371000, 10e24, (0, 0), (0, 0))
moon  = Ball (1737100, 10e21, (0, 20000000), (20220000, 0))
astro = Ball (RAD, 1000, (0, 100000), (2000000, 0))
solar = (earth, astro,)# moon)
things = balls
sim = Simulation (things, .01)

while True:

    DISPLAY.fill (WHITE)
    pygame.draw.line (DISPLAY, BLACK, (0, HEIGHT / 2), (WIDTH, HEIGHT / 2))
    pygame.draw.line (DISPLAY, BLACK, (WIDTH / 2, 0), (WIDTH / 2, HEIGHT))
    max_position = 0

    for event in pygame.event.get ():
        if event.type == QUIT:
            pygame.quit ()
            sys.quit ()

        elif event.type == VIDEORESIZE:
            WIDTH, HEIGHT = Decimal (event.size [0]), Decimal (event.size [1])
            DISPLAY = pygame.display.set_mode ((WIDTH, HEIGHT), RESIZABLE)
            MAX_DISPLAY_LENGTH = Decimal (min (WIDTH, HEIGHT)) / 2

    for b in sim.things:
        if b.position.length > max_position:
            max_position = b.position.length

        pygame.draw.circle (DISPLAY, BLACK, 
                (ceil (b [0] * FACTOR) + WIDTH / 2, ceil (b [1]) * FACTOR + HEIGHT / 2), b.radius * FACTOR)
    sim.step ()

    #FACTOR = (MAX_DISPLAY_LENGTH - DISPLAY_BORDER)  / max_position

    pygame.display.update ()
    CLOCK.tick (60)

