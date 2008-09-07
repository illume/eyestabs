

from pygame.locals import *

import game
Game = game.Game


class Intro(Game):
    


    def handle_events(self, events):
        Game.handle_events(self, events)

	for e in events:
	    if e.type == KEYDOWN:
	        if e.key == K_ESCAPE:
		    self.going = False
        
    def update(self, elapsed_time):
        Game.update(self, elapsed_time)
        
        
    def draw(self, screen):
        rects = Game.draw(self, screen)
	return rects








