"""
Game main module.
"""

import os,sys
import data
import pygame
from pygame.locals import *


import constants

# Game is an interface for different sections of the game.
#    Similar to a Movie in flash.
# Each section of the game will have a separate object controlling it.
#    For sections like the 'intro' and the 'end sequence' will have 
#      separate Game objects.
# See game.py for more information.


from game import Game
from intro import Intro
# The part where you guess what the notes are, by tapping on the keyboard.
#    Or playing your guitar.
from noteguess import NoteGuess

import analyse_thread

class Top(Game):
    def handle_events(self, events):
        # handle our events first, then the childrens.
        for e in events:
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    self.check_transition()
                if e.key == K_s:
                    pass
                    pygame.image.save(pygame.display.get_surface(), "eye_stab_screeny_2008_09_10.png")

            if e.type == QUIT:
                self.going = False

        # this handles the childrens events amongst others.
        Game.handle_events(self, events)
    
    def update(self, elapsed_time):
        Game.update(self, elapsed_time)

    def draw(self, screen):
        rects = Game.draw(self, screen)

        return rects




    def check_transition(self):
        """ See which part of the game we are at, and where we should go.
        """
        
        # which part of the game are we going into?
        if self.intro.going:
            self.intro.stop()
            # stop the intro music.
            pygame.mixer.music.fadeout(100)
            pygame.mixer.music.stop()

            self.note_guess.load()
            self.note_guess.start()
            self.note_guess.set_main()

        elif self.note_guess.going:
            self.note_guess.stop()
        else:
            print 'ok'
            self.stop()







def main():
    #print "Hello from your game's main()"
    #print data.load('sample.txt').read()
    
    #pygame.mixer.pre_init(44100,-16,2, 1024* 4)
    #pygame.mixer.pre_init(44100,-16,2, 1024* 4) 

    pygame.init()
    pygame.fastevent.init()
    
    analyse_thread.init()
    
    # start playing intro track, before the screen comes up.
    try:
        intro_track = os.path.join("data", "intro.ogg")
        pygame.mixer.music.load(intro_track)
        pygame.mixer.music.play(-1)
    except:
        print "failed playing music track: '%s'" % intro_track


    screen = pygame.display.set_mode(constants.SCREEN_SIZE)
    

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

        # we pass in the events so all of them can get the events.
        top.handle_events(events)

        # each part that uses time, for animation or otherwise
        #   gets the same amount of elapsed time.  This also reduces the
        #   number of system calls (gettimeofday) to one per frame.
        top.update(elapsed_time)
        
        
        # the draw method retunrns a list of rects, 
        #   for where the screen needs to be updated.
        rects = top.draw(screen)
        
        # remove empty rects.
        rects = filter(lambda x: x != [], rects)
        
        # if not empty, then update the display.
        if rects != []:
            pygame.display.update(rects)
        #pygame.display.update(rects)
        
        # we ask the clock to try and stay at a FPS rate( eg 30fps).
        #  It won't get exactly this, but it tries to get close.
        clock.tick(constants.FPS)


    # we try and clean up explicitly, and more nicely... 
    #    rather than hoping python will clean up correctly for us.
    pygame.quit()
    
    analyse_thread.quit()




