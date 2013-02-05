import pygame, sys, csv
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

DISPLAY_BORDER = 50 
MAX_DISPLAY_LENGTH = Decimal (min (WIDTH, HEIGHT)) / 2

things = []
with open ('things/world1', 'r') as f:
    reader = csv.reader (f)
    for line in reader:
        if len (line) < 7:
            raise Exception ('malformed things csv')

        name    = line [0]
        radius  = Decimal (line [1])
        mass    = Decimal (line [2])
        pos     = line [3:5]
        vel     = line [5:7]

        things.append (Ball (radius, mass, pos, vel))

sim = Simulation (things, .01)

factor = Decimal ("1")
display_center = vec2d (WIDTH / 2, HEIGHT / 2)
min_drag = vec2d (10, 10)

while True:

    DISPLAY.fill (WHITE)
    pygame.draw.line (DISPLAY, BLACK, (0, display_center [1]), 
            (WIDTH, display_center [1]))
    pygame.draw.line (DISPLAY, BLACK, (display_center [0], 0), 
            (display_center [0], HEIGHT))
    max_position = 0

    for event in pygame.event.get ():
        if event.type == QUIT:
            pygame.quit ()
            sys.quit ()

        elif event.type == VIDEORESIZE:
            WIDTH, HEIGHT = Decimal (event.size [0]), Decimal (event.size [1])
            DISPLAY = pygame.display.set_mode ((WIDTH, HEIGHT), RESIZABLE)

        elif event.type == MOUSEBUTTONUP:
            if event.button == 5:
                factor *= Decimal ('.9')
            elif event.button == 4:
                factor *= Decimal ('1.1')

        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                drag_start = vec2d (event.pos)

        elif event.type == MOUSEMOTION:
            if event.buttons [0] and min_drag.length < abs (drag_start - event.pos).length:
                display_center += (event.pos - drag_start)
                drag_start = vec2d (event.pos)


    for t in sim.things:
        if t.position.length > max_position:
            max_position = t.position.length

        display_pos = t.position * factor + display_center
        pygame.draw.circle (DISPLAY, BLACK, 
                (display_pos [0], 
                 display_pos [1]), 
                t.radius * factor)

    sim.step ()

    pygame.display.update ()
    CLOCK.tick (60)

