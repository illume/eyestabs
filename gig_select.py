################################################################################

"""

The gig selection part of the game.  

Where you get offered gigs, and you decide to take them or not.

"""

################################################################################
# STD LIBS

import os
import sys
import time

# 3RD PARTY LIBS
import pygame
from pygame.locals import *

from ocempgui.widgets import Renderer, Table, HScale, Label, VFrame, \
                             RadioButton, Button

from ocempgui.widgets.Constants import SIG_VALCHANGED, ALIGN_LEFT, SIG_ACTIVATED

# USER LIBS

import constants
import game

Game = game.Game

################################################################################

GIG_CHOICES =    {    
    "Dr StrangeLove"              :  "doctor_yellow2.jpg",
    "Love is\nin the air"         :  "love-parade.jpg",
    "Le Francoise"                :  "eiffel-tower.jpg",
    "MOSH!!"                      :  "moshing-punks.jpg",
}

for gig, pic in GIG_CHOICES.items():
    GIG_CHOICES[gig] = pygame.image.load(os.path.join("data", "images", pic))

################################################################################

def create_vframe (text):
    frame = VFrame (Label (text))
    frame.spacing = 5
    frame.align = ALIGN_LEFT
    return frame

class GigWidget(object):
    def __init__(self):
        self.table = Table(2, 1)
        radio_frame = create_vframe('Select A Gig')

        group = None
        for i, s in enumerate(sorted(GIG_CHOICES.keys())):

            btn = RadioButton (s, group)
            if i == 0:
                group = btn

            btn.child.multiline = True
            radio_frame.add_child (btn)

        group.activate()

        self.button = Button('SELECT GIG')

        self.radios = group.list

        self.table.add_child(0, 0, radio_frame)
        self.table.add_child(1, 0, self.button)

################################################################################

class GigSelect(Game):
    def __init__(self, screen, *args, **kw):
        Game.__init__(self, *args, **kw)

        self.re = Renderer ()
        self.re.screen = screen

        self.gig_widget = GigWidget()

        self.gig_widget.button.connect_signal('clicked', self.stop)

        for radio in self.gig_widget.radios:
            radio.connect_signal('toggled', self.update_selection)

        self.re.add_widget( self.gig_widget.table )

        # {'SIGNALS_KEYS': (2, 3),
        #  'SIGNALS_MOUSE': (5, 4, 6),
        #  'SIG_ACTIVATED': 'activated',
        #  'SIG_CLICKED': 'clicked',
        #  'SIG_DESTROYED': 'destroyed',
        #  'SIG_DIALOGRESPONSE': 'dialog-response',
        #  'SIG_DOUBLECLICKED': 'double-clicked',
        #  'SIG_ENTER': 'entered',
        #  'SIG_FOCUSED': 'focused',
        #  'SIG_INPUT': 'input',
        #  'SIG_KEYDOWN': 2,
        #  'SIG_KEYUP': 3,
        #  'SIG_LEAVE': 'left',
        #  'SIG_LISTCHANGED': 'list-changed',
        #  'SIG_MOUSEDOWN': 5,
        #  'SIG_MOUSEMOVE': 4,
        #  'SIG_MOUSEUP': 6,
        #  'SIG_SCREENCHANGED': 28,
        #  'SIG_SELECTCHANGED': 'selection-changed',
        #  'SIG_TICK': 25,
        #  'SIG_TOGGLED': 'toggled',
        #  'SIG_TWISTED': 26,
        #  'SIG_UPDATED': 27,
        # 'SIG_VALCHANGED': 'value-changed'}

      # RADIOBUTTON SIGNALS    
      
        # {2: None,
        #  4: [],
        #  5: [],
        #  6: [],
        #  'clicked': [],
        #  'destroyed': [],
        #  'entered': [],
        #  'focused': [],
        #  'left': [],
        #  'toggled': []}

        self.update_selection()

    def update_selection(self, *args):
        print args
        
        radios = self.gig_widget.radios
        selection = [btn.text for btn in radios if btn.state == 2][0]
        self.selected = GIG_CHOICES[ selection ]
        self.changed = True
        
        print selection

    def handle_events(self, events):
        Game.handle_events(self, events)

        for e in events:
            if e.type == KEYDOWN and e.key == K_ESCAPE:
                self.stop()
                break

        self.re.distribute_events (*events)

        # TODO: WHERE SHOULD THIS GO?
        # if self.gig_widget.button.state == 2:
            # self.stop()

    def update(self, elapsed_time):
        Game.update(self, elapsed_time)

    def draw(self, screen):
        rects = Game.draw(self, screen)
        
        if self.changed:
            # self.re.screen.fill ((234, 228, 223))
            self.re.screen.blit(self.selected, (0,0))
            self.changed = 0
        
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
    prev_selected = None

    while gig_select.going:
        events = pygame.fastevent.get()

        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()

        gig_select.update(3)

        gig_select.handle_events(events)
        rects = [l for l in gig_select.draw(screen) if l]

        if rects:
            pygame.display.update(rects)
        
        # pygame.time.delay(15)
        
if __name__ == '__main__':
    development()