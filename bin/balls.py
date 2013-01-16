import pygame
from pygame.locals import *
from math import ceil
from time import sleep

from gravsim.vec2d import vec2d
from gravsim.things import Ball
from gravsim.simulation import Simulation

HEIGHT = 600
WIDTH  = 400
RAD    =  10

WHITE  = Color (255, 255, 255)
BLACK  = Color (000, 000, 000)

CLOCK = pygame.time.Clock ()
DISPLAY = pygame.display.set_mode ((WIDTH, HEIGHT))

x1wall = (vec2d (0, 0), vec2d (WIDTH, 0))
x2wall = (vec2d (0, HEIGHT), vec2d (WIDTH, 0))
y1wall = (vec2d (0, 0), vec2d (0, HEIGHT))
y2wall = (vec2d (WIDTH, 0), vec2d (0, HEIGHT))
diagon = (vec2d (WIDTH, HEIGHT) / 2, vec2d (WIDTH, HEIGHT))

borders = (x1wall, x2wall, y1wall, y2wall, diagon)
balls = ( Ball (RAD, (320, 120), (10, 10)), Ball (RAD, (350, 50), (10, 0)))
sim = Simulation (balls, borders, .1)

while True:

    DISPLAY.fill (WHITE)
    sim.step ()

    for b in sim.things:
        pygame.draw.circle (DISPLAY, BLACK, 
                (ceil (b [0]), ceil (b [1])), b.radius)

    for w in sim.walls:
        pygame.draw.line (DISPLAY, BLACK,
                (w [0]), (sum (w)))

    pygame.display.update ()
    CLOCK.tick (60)

