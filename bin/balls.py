import pygame 
from pygame.locals import *
from decimal import Decimal

import gen_client
from gravsim.vec2d import vec2d

class GraphicSim (object):

    def __init__ (self):
        self.height = Decimal (700)
        self.width  = Decimal (700)
        self.rad    = Decimal ( 10)

        self.white  = Color (255, 255, 255)
        self.black  = Color (000, 000, 000)
        self.red    = Color (255, 000, 000)

    def init (self, sim):

        self.factor = min (self.height, self.width) / max (t.position.length for t in sim.things)
        self.zoom_factor = Decimal (".1")
        self.display_center = vec2d (self.width / 2, self.height / 2)
        self.min_drag = vec2d (10, 10)
        self.drag_start = (0, 0)

        pygame.init ()
        self.clock = pygame.time.Clock ()
        self.font  = pygame.font.Font (pygame.font.get_default_font (), 12)
        self.bigfont  = pygame.font.Font (pygame.font.get_default_font (), 20)
        self.display = pygame.display.set_mode ((self.width, self.height), RESIZABLE)

    def step (self, sim):
    
        self.display.fill (self.white)
        pygame.draw.line (self.display, self.black, (0, self.display_center [1]), 
                (self.width, self.display_center [1]))
        pygame.draw.line (self.display, self.black, (self.display_center [0], 0), 
                (self.display_center [0], self.height))

        for event in pygame.event.get ():
            if event.type == QUIT:
                pygame.quit ()
                sys.exit ()

            elif event.type == VIDEORESIZE:
                self.width, self.height = Decimal (event.size [0]), Decimal (event.size [1])
                self.display = pygame.display.set_mode ((self.width, self.height), RESIZABLE)

            elif event.type == MOUSEBUTTONUP:
                if event.button in (4, 5):
                    zoom = 1 + (self.zoom_factor * (-1 if event.button == 5 else 1))
                    self.factor *= zoom

            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.drag_start = vec2d (event.pos)

            elif event.type == MOUSEMOTION:
                if event.buttons [0] and self.min_drag.length < abs (self.drag_start - event.pos).length:
                    self.display_center += (event.pos - self.drag_start)
                    self.drag_start = vec2d (event.pos)

        for i, t in enumerate (sim.things):
            display_pos = t.position * self.factor + self.display_center

            pygame.draw.circle (self.display, self.black, 
                    (display_pos [0], 
                     display_pos [1]), 
                     t.radius * self.factor)

            font_render = self.font.render (t.name, True, self.red)
            font_rect   = font_render.get_rect ()
            font_rect.center = display_pos
            self.display.blit (font_render, font_rect)

            speed_render = self.bigfont.render (
                    "%s: v = %.4f m/s a = %4.4f m/s^2" % (t.name, t.velocity.length, sum (t.a.values ()).length ),
                    True, self.black)
            speed_rect   = speed_render.get_rect ()
            speed_rect.bottomleft = (20, 50 + 30 * i)
            self.display.blit (speed_render, speed_rect)

        time_render = self.bigfont.render ("dt: {} Time: {}".format (sim.stepsize, sim.time), True, self.black)
        time_rect = time_render.get_rect ()
        time_rect.bottomleft = (20, self.height - 60)
        self.display.blit (time_render, time_rect)

        pygame.display.update ()
        self.clock.tick (20000)


module = GraphicSim ()
gen_client.run (module)
