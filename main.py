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
# The part where you guess what the notes are, by tapping on the keyboard.
#    Or playing your guitar.
from noteguess import NoteGuess



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
	""" See which part of the game we are at, and where we should go.
	"""
        
        # which part of the game are we going into?
	if self.intro.going:
	    self.intro.stop()
	    self.note_guess.load()
	    self.note_guess.start()
	    self.note_guess.set_main()

	elif self.note_guess.going:
	    self.note_guess.stop()
	else:
	    print 'ok'
	    self.stop()





    def draw(self, screen):
        rects = Game.draw(self, screen)




	return rects









def main():
    print "Hello from your game's main()"
    print data.load('sample.txt').read()
    
    pygame.mixer.pre_init(44100,-16,2, 1024* 4)
    #pygame.mixer.pre_init(44100,-16,2, 1024* 4) 

    pygame.init()
    pygame.fastevent.init()
    
    # start playing intro track, before the screen comes up.
    try:
        intro_track = os.path.join("data", "intro.ogg")
        pygame.mixer.music.load(intro_track)
        pygame.mixer.music.play(-1)
    except:
        print "failed playing music track: '%s'" % intro_track


    screen = pygame.display.set_mode(SCREEN_SIZE)
    

    top = Top(name = "Eye stabs.  Do you?")
    top.set_main()
    
    # Add the intro as a child Game to the top Game.
    intro = Intro(name ="eye stab intro")
    
    top.games.append(intro)
    top.intro = intro
    
    note_guess = NoteGuess(name="Eye stabs.    Note Guess")

    # stop the note_guess part, because we are not ready yet.
    note_guess.stop()
    top.games.append(note_guess)
    top.note_guess = note_guess
    
    
    
    clock = pygame.time.Clock()
    clock.tick()
    
    while top.going:
        elapsed_time = clock.get_time()
	if elapsed_time:
	    elapsed_time = elapsed_time / 1000.

        events = pygame.fastevent.get()

        top.handle_events(events)

	top.update(elapsed_time)

	rects = top.draw(screen)

	# remove empty rects.
	rects = filter(lambda x: x != [], rects)

	# if not empty, then update the display.
	if rects != []:
	    pygame.display.update(rects)
	#pygame.display.update(rects)

	clock.tick(FPS)

    pygame.quit()