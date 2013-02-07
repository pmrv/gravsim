import pygame, sys, csv, os
from pygame.locals import *
from math import ceil, sqrt
from time import sleep
from decimal import Decimal

from gravsim.vec2d import vec2d
from gravsim.things import Ball
from gravsim.simulation import Simulation


def draw_font (self, text, color, centerx, centery, big = False):
    """
    big - bool, whether to use the big font or the small font
    """
    
    if big:
        font = self.bigfont
    else:
        font = self.font

    return font_rect 


HEIGHT = Decimal (700)
WIDTH  = Decimal (700)
RAD    = Decimal ( 10)

WHITE  = Color (255, 255, 255)
BLACK  = Color (000, 000, 000)
RED    = Color (255, 000, 000)

world_files = os.listdir ("worlds")
if len (world_files) == 0:
    sys.exit ()
if len (sys.argv) > 1 and sys.argv [1] in world_files:
    world = sys.argv [1]
else:
    world = world_files [0]

things = []
with open ("./worlds/" + world, 'r') as f:
    reader = csv.reader (f)
    for line in reader:
        if len (line) < 7:
            raise Exception ('malformed line in csv')

        name    = line [0]
        radius  = Decimal (line [1])
        mass    = Decimal (line [2])
        pos     = line [3:5]
        vel     = line [5:7]

        things.append (Ball (name, radius, mass, pos, vel))

sim = Simulation (things, .1)
pygame.init ()
CLOCK = pygame.time.Clock ()
DISPLAY = pygame.display.set_mode ((WIDTH, HEIGHT), RESIZABLE)


pygame.init ()
CLOCK = pygame.time.Clock ()
FONT  = pygame.font.Font (pygame.font.get_default_font (), 11)
DISPLAY = pygame.display.set_mode ((WIDTH, HEIGHT), RESIZABLE)

factor = min (HEIGHT, WIDTH) / max (t.position.length for t in sim.things)
zoom_factor = Decimal (".1")
display_center = vec2d (WIDTH / 2, HEIGHT / 2)
min_drag = vec2d (10, 10)

while True:

    DISPLAY.fill (WHITE)
    pygame.draw.line (DISPLAY, BLACK, (0, display_center [1]), 
            (WIDTH, display_center [1]))
    pygame.draw.line (DISPLAY, BLACK, (display_center [0], 0), 
            (display_center [0], HEIGHT))

    for event in pygame.event.get ():
        if event.type == QUIT:
            pygame.quit ()
            sys.exit ()

        elif event.type == VIDEORESIZE:
            WIDTH, HEIGHT = Decimal (event.size [0]), Decimal (event.size [1])
            DISPLAY = pygame.display.set_mode ((WIDTH, HEIGHT), RESIZABLE)

        elif event.type == MOUSEBUTTONUP:
            if event.button in (4, 5):
                zoom = 1 - zoom_factor if event.button == 5 else 1 + zoom_factor
                factor *= zoom

        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                drag_start = vec2d (event.pos)

        elif event.type == MOUSEMOTION:
            if event.buttons [0] and min_drag.length < abs (drag_start - event.pos).length:
                display_center += (event.pos - drag_start)
                drag_start = vec2d (event.pos)

    for t in sim.things:
        display_pos = t.position * factor + display_center

        pygame.draw.circle (DISPLAY, BLACK, 
                (display_pos [0], 
                 display_pos [1]), 
                t.radius * factor)

        font_render = FONT.render (t.name, True, RED)
        font_rect = font_render.get_rect ()
        font_rect.center = display_pos
        DISPLAY.blit (font_render, font_rect)

    sim.step ()

    pygame.display.update ()
    CLOCK.tick (60)

