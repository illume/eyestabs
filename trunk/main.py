"""
Game main module.
"""

import data
import pygame
from pygame.locals import *



from game import Game
from intro import Intro


class Top(Intro):
    

    def handle_events(self, events):
        Game.handle_events(self, events)

	for e in events:
	    if e.type == KEYDOWN:
	        if e.key == ESCAPE:
		    self.going = False

	    if e.type == QUIT:
	        self.going = False

    def update(self, elapsed_time):
        Game.update(self, elapsed_time)

    def draw(self, screen):
        rects = Game.draw(self, screen)
	return rects









def main():
    print "Hello from your game's main()"
    print data.load('sample.txt').read()

    fps = 30
    screen_size = (640,480)

    pygame.init()
    
    # start playing intro track.

    screen = pygame.display.set_mode(screen_size)
    
    top = Top(name = "Eye stabs.  Do you?")
    top.set_main()
    
    intro = Intro(name ="eye stab intro")
    
    top.games.append(intro)
    
    
    
    clock = pygame.time.Clock()
    
    while top.going:
        elapsed_time = clock.get_time()

        events = pygame.event.get()

        top.handle_events(events)

	top.update(elapsed_time)

	rects = top.draw(screen)

	# remove empty rects.
	rects = filter(lambda x: x != [], rects)

	# if not empty, then update the display.
	if rects != []:
	    print "updating display"
	    pygame.display.update(rects)

	clock.tick(fps)


    pygame.quit()


