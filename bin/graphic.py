import pygame
from pygame.locals import *
from decimal import Decimal
from time import time

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

    def correct_positions (self, pos):
        if len (pos) != 2: raise Exception ("Pos must have len == 2.")
        return (self.factor * pos [0] + self.display_correction.x, self.factor * pos [1] + self.display_correction.y)

    def init (self, sim):

        self.factor = min (self.height, self.width) / max (t.position.length for t in sim.things)
        self.zoom_factor = Decimal (".1")
        self.middle = vec2d (self.width / 2, self.height / 2)
        self.display_center = vec2d (self.middle)
        self.min_drag = vec2d (10, 10)
        self.drag_start = vec2d (0, 0)
        self.thing_orbits = {t.name: [ (t.position.x, t.position.y) ] for t in sim.things}
        self.max_orbit_points = 1000

        pygame.init ()
        self.clock = pygame.time.Clock ()
        self.font  = pygame.font.Font (pygame.font.get_default_font (), 12)
        self.bigfont = pygame.font.Font (pygame.font.get_default_font (), 20)
        self.display = pygame.display.set_mode ((self.width, self.height), RESIZABLE)

        self.focus = None
        self.buttons = {}
        for t in sim.things:

            button_render = self.bigfont.render (t.name, True, self.black, self.red)
            button_rect   = button_render.get_rect ()
            # if we have a lot Things an enumerate might be better
            button_rect.topleft = (0, self.height - 50 - 20 * sim.things.index (t))
            self.buttons [t] = (button_render, button_rect)

    def step (self, sim):

        if sim.time % 5: return

        for event in pygame.event.get ():
            if event.type == QUIT:
                pygame.quit ()
                return "quit"

            elif event.type == VIDEORESIZE:
                self.width, self.height = Decimal (event.size [0]), Decimal (event.size [1])
                self.display = pygame.display.set_mode ((self.width, self.height), RESIZABLE)

            elif event.type == MOUSEBUTTONUP:
                if event.button in (4, 5):
                    # readable code is a wonderful invention, isn't it?
                    zoom = 1 + (self.zoom_factor * int ((4.5 - event.button) * 2))
                    self.factor *= zoom

            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    for thing, rects in self.buttons.items ():
                        if rects [1].collidepoint (*event.pos):
                            self.focus = thing.position
                            break
                    else: 
                        if self.focus:
                            self.display_center = vec2d (self.focus)
                        self.focus = None
                        self.drag_start = vec2d (event.pos)

            elif event.type == MOUSEMOTION:
                if event.buttons [0] and self.min_drag.length < abs (self.drag_start - event.pos).length:
                    drag = event.pos - self.drag_start
                    self.focus 
                    self.display_center -= drag / self.factor
                    self.drag_start = vec2d (event.pos)

        self.display.fill (self.white)

        pos = self.focus if self.focus else self.display_center
        self.display_correction = self.middle - self.factor * pos
        
        pygame.draw.line (self.display, self.black, (0, self.display_correction [1]), 
                (self.width, self.display_correction [1]))
        pygame.draw.line (self.display, self.black, (self.display_correction [0], 0), 
                (self.display_correction [0], self.height))

        pygame.draw.line (self.display, self.red, (0, self.middle [1]), 
                (self.width, self.middle [1]))
        pygame.draw.line (self.display, self.red, (self.middle [0], 0), 
                (self.middle [0], self.height))


        for t in sim.things:

            display_pos = self.correct_positions (t.position)
            pygame.draw.circle (self.display, self.black, display_pos,
                    t.radius * self.factor)

            pygame.draw.lines (self.display, self.black, False,
                         list (map (self.correct_positions, self.thing_orbits [t.name] + [t.position])), 
                         1)

            name_render = self.font.render (t.name, True, self.red)
            name_rect   = name_render.get_rect ()
            name_rect.center = display_pos
            self.display.blit (name_render, name_rect)
            self.display.blit ( *self.buttons [t] )

            pxspeed = self.factor * t.velocity.length
            if not sim.time % int (pxspeed + 1):
                self.thing_orbits [t.name].append (
                        (t.position.x, t.position.y)
                )

            if len (self.thing_orbits [t.name]) > self.max_orbit_points:
                self.thing_orbits [t.name].pop (0)

        pygame.display.update ()
        self.clock.tick (60)


if __name__ == "__main__":
    module = GraphicSim ()
    gen_client.run ([module])
