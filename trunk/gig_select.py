################################################################################

"""

The gig selection part of the game.  

Where you get offered gigs, and you decide to take them or not.

"""

################################################################################
# STD LIBS

import os
import sys

# 3RD PARTY LIBS
import pygame
from pygame.locals import *

from ocempgui.widgets import Renderer, Table, HScale, Label
from ocempgui.widgets.Constants import SIG_VALCHANGED

# USER LIBS

import constants
import game

Game = game.Game

################################################################################

def _update_parameter(scale, label):
    label.text = "Value: %f" % scale.value


class GigWidget(object):
    def __init__(self):
        self.table = Table(2, 1)

        self.scale = HScale(0, 20)
        self.scale.value = 5
        label = Label ("Value: %f" % self.scale.value)

        self.scale.connect_signal (
            SIG_VALCHANGED, _update_parameter, self.scale, label
        )

        self.table.topleft = 5, 5
        self.table.spacing = 5

        self.table.add_child(0, 0, self.scale)
        self.table.add_child(1, 0, label)

################################################################################

class GigSelect(Game):
    def __init__(self, screen, *args, **kw):
        Game.__init__(self, *args, **kw)

        # Create the Renderer to use for the UI elements.
        self.re = Renderer ()

        # Bind it to a part of the screen, which it will use to draw the widgets.
        # Here we use the complete screen.
        self.re.screen = screen

        self.gig_widget = GigWidget()

        self.re.add_widget( self.gig_widget.table )

    fans = property(lambda self: self.gig_widget.scale.value)

    def handle_events(self, events):
        Game.handle_events(self, events)

        for e in events:
            if e.type == KEYDOWN and e.key == K_ESCAPE:
                self.stop()
                break

        self.re.distribute_events (*events)

    def update(self, elapsed_time):
        Game.update(self, elapsed_time)

    def draw(self, screen):
        rects = Game.draw(self, screen)

        self.re.screen.fill ((234, 228, 223))
        self.re.refresh ()

        return rects

    def stop(self):
        """
        """
        print 'gig_select stopped'
        self.going = False

################################################################################

def development():
    pygame.init()
    pygame.fastevent.init()

    screen = pygame.display.set_mode((640, 400))

    gig_select = GigSelect(screen)

    while True:
        events = pygame.fastevent.get()
        
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()
        
        gig_select.update(3)
        
        gig_select.handle_events(events)
        rects = [l for l in gig_select.draw(screen) if l]

        if rects:
            pygame.display.update(rects)
            
        print gig_select.fans
        
if __name__ == '__main__':
    development()