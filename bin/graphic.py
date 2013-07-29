from pygame.locals import *
import pygame
import numpy
import time
import gravsim.view

def length (array, axis = None):
    return numpy.sqrt ( (array ** 2).sum (axis = axis) )

class GraphicSim (gravsim.view.View):

    def correct_positions (self, pos):
        return self.factor * pos + self.display_correction

    def __init__ (self):

        gravsim.view.View.__init__ (self, description = "Pygame Viewer to the gravsim 'engine'.")

        self.height = 700
        self.width  = 700
        self.rad    =  10

        self.white  = Color (255, 255, 255)
        self.black  = Color (000, 000, 000)
        self.red    = Color (255, 000, 000)

        self.factor = min (self.height, self.width) / max (l for l in length (self.sim.positions, axis = -1))
        self.zoom_factor = .1
        self.middle = numpy.array ( (self.width / 2, self.height / 2), dtype = numpy.float64 )
        self.display_center = numpy.array ( (0, 0) ) # the point in simulation coordinates to display at the center
        self.min_drag = numpy.array ( (10, 10) )

        self.max_orbit_points = 1000
        self.num_orbit = numpy.zeros ( (len (self.sim.things),), dtype = numpy.int64 )
        self.past_orbits = numpy.zeros ( (len (self.sim.things), self.max_orbit_points, 2), dtype = numpy.int64 )

        self.displaytime = 20
        self.last_display = 0

        pygame.init ()
        self.font  = pygame.font.Font (pygame.font.get_default_font (), 12)
        self.bigfont = pygame.font.Font (pygame.font.get_default_font (), 20)
        self.display = pygame.display.set_mode ((self.width, self.height), RESIZABLE)

        self.focus = None
        self.buttons = [0] * len (self.sim.things)
        for name, index in self.sim.things.items ():

            button_render = self.bigfont.render (name, True, self.black, self.red)
            button_rect   = button_render.get_rect ()
            button_rect.topleft = (0, self.height - 50 - 20 * index)

            name_render = self.font.render (name, True, self.red)
            name_rect   = name_render.get_rect ()

            self.buttons [index] = (button_render, button_rect, name_render, name_rect)

    def step (self):

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
                    for index, rects in enumerate (self.buttons):
                        if rects [1].collidepoint (*event.pos):
                            self.focus = self.sim.positions [index]
                            break
                    else: 
                        if self.focus != None:
                            self.display_center = self.focus.copy ()
                        self.focus = None
                        self.drag_start = numpy.array ( [event.pos [0], event.pos [1]] )

            elif event.type == MOUSEMOTION:
                if event.buttons [0] and length (self.min_drag) < length (self.drag_start - event.pos):
                    drag = event.pos - self.drag_start
                    self.display_center -= drag / self.factor
                    self.drag_start = numpy.array ( [event.pos [0], event.pos [1]] )

        self.sim.step (self.stepsize)

        # this is somewhat unflexible..
        if round (self.sim.time, 2) % self.displaytime != 0.: return

        self.display.fill (self.white)

        pos = self.focus if self.focus != None else self.display_center
        self.display_correction = self.middle - self.factor * pos
        
        pygame.draw.line (self.display, self.black, (0, self.display_correction [1]), 
                (self.width, self.display_correction [1]))
        pygame.draw.line (self.display, self.black, (self.display_correction [0], 0), 
                (self.display_correction [0], self.height))

        for name, index in self.sim.things.items ():

            pos = self.sim.positions [index]
            display_pos = numpy.cast [numpy.int64] (self.correct_positions (pos))
            rad = int (self.sim.radii [index] * self.factor)
            pygame.draw.circle (self.display, self.black, display_pos, rad)

            #pygame.draw.lines (self.display, self.black, False,
            #        list (map (self.correct_positions, self.past_orbits [index])) + [display_pos], 
            #        1)

            *button, name_render, name_rect = self.buttons [index]
            name_rect.center = display_pos
            self.display.blit (name_render, name_rect)
            self.display.blit (*button)

            #pxspeed = self.factor * length (self.sim.velocities [index])
            #if not self.sim.time % int ( (1 / pxspeed) + 1):
            #    self.past_orbits [index, self.num_orbit [index]] = pos
            #    self.num_orbit [index] = (self.num_orbit [index] + 1) % self.max_orbit_points

        
        delta = time.time () - self.last_display
        time_render = self.bigfont.render (str (self.displaytime/delta), True, self.black)
        time_rect   = time_render.get_rect ()
        time_rect.topleft = (0, 0)
        self.display.blit (time_render, time_rect)
        pygame.display.update ()

        self.last_display = time.time ()

if __name__ == "__main__":
    s = GraphicSim ()
    s.run ()
