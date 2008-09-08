"""

An object representing a game... or game sequence.


This is how each Game object is called.

# the constructor calls the load() method too.
g = Game()

in loop:
    g.handle_events(events)
    g.update(elapsed_time_since_last_frame)
    rects_dirtied = g.draw(screen)

"""

import pygame
from pygame.locals import *


class Game(object):

    
    def __init__(self, going = True, games = None, name = "", elapsed_time = 0.0):
        """ games - children game objects.
	    going - if this is going.
	"""

        self.going = going

        # a list of children game objects.
	if not games:
	    games = []

	self.games = games

	self.name = name

	self.elapsed_time = elapsed_time

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

    def stop(self):
        self.going = False
    def start(self):
        self.going = True



    def update(self, elapsed_time):
	self.elapsed_time += elapsed_time
#	print self.games

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








