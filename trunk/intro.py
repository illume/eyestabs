
import pygame
from pygame.locals import *

import game
Game = game.Game



class Intro(Game):
    def load(self):
        Game.load(self)
	self.font_size = 40
	self.font = pygame.font.Font(None, self.font_size)
	self.font_color = (255,255,255,255)


    def handle_events(self, events):
        Game.handle_events(self, events)

	for e in events:
	    if e.type == KEYDOWN:
	        if e.key == K_ESCAPE:
		    self.stop()
        
    def update(self, elapsed_time):
        Game.update(self, elapsed_time)

	if self.elapsed_time < 2.0:
	    self.text_string = "Eye stabs.   Do you?"
	elif self.elapsed_time >= 2.0 and self.elapsed_time < 4.0:
	    self.text_string = "Yeah I do stabs."
	  
	elif self.elapsed_time >= 4.0 and self.elapsed_time < 8.0:
	    self.text_string = "Cool.  I like you then."

	elif self.elapsed_time >= 8.0 and self.elapsed_time < 800.0:
	    self.stop()


    def stop(self):
        """
	"""
	print 'intro stopped'
	self.going = False

    def draw(self, screen):
        rects = Game.draw(self, screen)
	the_text = self.font.render(self.text_string, 1, self.font_color)

	screen.fill((0,0,0,255))

	x,y = screen.get_rect().center

	x = x - (the_text.get_width() / 2)

	r = screen.blit(the_text, (x,y))

	# update the whole screen.
	rects.extend(screen.get_rect())

	return rects








