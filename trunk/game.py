"""

An object representing a game... or game sequence.



"""

import pygame
from pygame.locals import *


class Game(object):

    
    def __init__(self, going = True, games = None, name = ""):
        """ games - children game objects.
	    going - if this is going.
	"""

        self.going = going

        # a list of children game objects.
	if not games:
	    games = []

	self.games = games

	self.name = name

	self.load()


    def load(self):
        """ called to load data.
	"""
        pass

    
    def set_main(self):
        """ sets this to the main game being used.
	"""
	pygame.display.set_caption(self.name)
	pygame.event.pump()


    def handle_events(self, events):

	for g in self.games:
            if g.going:
                g.handle_events(events)


    def update(self, elapsed_time):

	for g in self.games:
            if g.going:
                g.update(elapsed_time)


    def draw(self, screen):
        rects = []

	for g in self.games:
            if g.going:
	        sub_rects = g.draw(screen)
		rects.extend( sub_rects )

        return rects








