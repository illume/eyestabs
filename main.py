"""
Game main module.
"""

import os,sys
import data
import pygame
from pygame.locals import *


# Game is an interface for different sections of the game.
#    Similar to a Movie in flash.
# Each section of the game will have a separate object controlling it.
#    For sections like the 'intro' and the 'end sequence' will have 
#      separate Game objects.

from game import Game
from intro import Intro


class Top(Game):
    

    def handle_events(self, events):

        # handle our events first, then the childrens.
	for e in events:
	    if e.type == KEYDOWN:
	        if e.key == K_ESCAPE:
		    self.check_transition()

	    if e.type == QUIT:
	        self.going = False

        # this handles the childrens events amongst others.
        Game.handle_events(self, events)

    
    def update(self, elapsed_time):
        Game.update(self, elapsed_time)


    def stop(self):
        print 'stopping Top'
	self.going = False


    def check_transition(self):

        # which part of the game are we going into?
	if self.intro.going:
	    self.intro.stop()
	else:
	    print 'ok'
	    self.stop()


    def draw(self, screen):
        rects = Game.draw(self, screen)




	return rects









def main():
    print "Hello from your game's main()"
    print data.load('sample.txt').read()

    fps = 30
    screen_size = (640,480)

    pygame.init()
    
    # start playing intro track, before the screen comes up.
    try:
        intro_track = os.path.join("data", "intro.ogg")
        pygame.mixer.music.load(intro_track)
        pygame.mixer.music.play()
    except:
        print "failed playing music track: '%s'" % intro_track


    screen = pygame.display.set_mode(screen_size)
    
    top = Top(name = "Eye stabs.  Do you?")
    top.set_main()
    
    intro = Intro(name ="eye stab intro")
    
    top.games.append(intro)
    top.intro = intro
    
    
    
    clock = pygame.time.Clock()
    clock.tick()
    
    while top.going:
        elapsed_time = clock.get_time()
	if elapsed_time:
	    elapsed_time = elapsed_time / 1000.

        events = pygame.event.get()

        top.handle_events(events)

	top.update(elapsed_time)

	rects = top.draw(screen)

	# remove empty rects.
	rects = filter(lambda x: x != [], rects)

	# if not empty, then update the display.
	if rects != []:
	    pygame.display.update(rects)
	#pygame.display.update(rects)

	clock.tick(fps)


    pygame.quit()


