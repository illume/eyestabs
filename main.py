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

from gig_select import GigSelect

from video_player import VideoPlayer

from eyefix_result import EyeFixResult

from doctors_surgery import DoctorsSurgery

import analyse_thread


import player



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


        if 0:
            print data.where_to
            print self.gig_select.going
            print self.games


        if data.where_to == "intro":
            self.stop_all()
            self.intro.start()
            data.where_to = ""


        if data.where_to == "gig_select":
            self.stop_all()
            self.gig_select.start()
            data.where_to = ""
        if data.where_to == "note_guess":
            self.stop_all()
            self.note_guess.start()
            data.where_to = ""
        if data.where_to == "doctors_surgery":
            self.stop_all()
            self.doctors_surgery.start()
            data.where_to = ""

        if data.where_to == "eyefix":
            print 'eye fix1!!!'
            self.stop_all()
            self.eyefix.choose_result()
            self.eyefix.start()
            data.where_to = ""




    def draw(self, screen):
        rects = Game.draw(self, screen)

        return rects



    def stop_all(self):
        for g in self.games:
            g.stop()

    def check_transition(self):
        """ See which part of the game we are at, and where we should go.
        """


        
        # which part of the game are we going into?
        if self.intro.going:
            self.intro.stop()
            # stop the intro music.
            # pygame.mixer.music.fadeout(100)
            # pygame.mixer.music.stop()
            if hasattr(self.intro, "loop_ogg"):
                self.intro.loop_ogg.fadeout(100)
                self.intro.loop_ogg.stop()

            self.note_guess.load()
            self.note_guess.start()
            self.note_guess.set_main()

        elif self.note_guess.going:
            self.note_guess.stop()
            data.where_to = "gig_select"
        else:
            print 'ok'
            self.stop()

        







def main():


    # in a compiled exe this can be called.
    if "analyse_play.py" in sys.argv:
        import analyse_play
        analyse_play.main()
        return


    data.where_to = ""


    #print "Hello from your game's main()"
    #print data.load('sample.txt').read()
    
    #pygame.mixer.pre_init(44100,-16,2, 1024* 4)
    pygame.mixer.pre_init(44100,-16,2, 1024* 4) 

    pygame.init()
    pygame.fastevent.init()

    pygame.threads.init(4)



    analyse_thread.init()

    # start playing intro track, before the screen comes up.
    if 0:
        try:
            intro_track = os.path.join("data", "intro.ogg")
            pygame.mixer.music.load(intro_track)
            pygame.mixer.music.play(-1)
        except:
            print "failed playing music track: '%s'" % intro_track

    else:
        import numpy
        pygame.sndarray.use_arraytype("numpy")
        
        mixer = pygame.mixer

        def _array_samples(sound, raw):
            # Info is a (freq, format, stereo) tuple
            info = mixer.get_init ()
            if not info:
                raise pygame.error, "Mixer not initialized"
            fmtbytes = (abs (info[1]) & 0xff) >> 3
            channels = info[2]
            if raw:
                data = sound.get_buffer ().raw
            else:
                data = sound.get_buffer ()
        
            shape = (len (data) / (channels * fmtbytes), )
            if channels > 1:
                shape = (shape[0], 2)

            # mixer.init () does not support different formats from the ones below,
            # so MSB/LSB stuff is silently ignored.
            typecode = { 8 : numpy.uint8,   # AUDIO_U8
                         16 : numpy.uint16, # AUDIO_U16 / AUDIO_U16SYS
                         -8 : numpy.int8,   # AUDIO_S8
                         -16 : numpy.int16  # AUDUI_S16 / AUDIO_S16SYS
                         }[info[1]]

            print channels
            print fmtbytes
            print typecode
            
            array = numpy.fromstring (data, typecode)
            print array.shape
            print shape
            
            array.shape = shape
            return array
        
        intro_track = os.path.join("data", "intro.ogg")
        intro_sound = pygame.mixer.Sound(intro_track)
        
        
        intro_array = _array_samples(intro_sound, 1)[:705600/2]

        

        # assert len(intro_array) == 705600

        for i in range(1):  # 4 x longer
            intro_array = numpy.append(intro_array, intro_array, 0)

        intro_sound_big = pygame.sndarray.make_sound(intro_array)
        
        pygame.time.set_timer(constants.INTRO_FADEOUT, 31000)
        intro_sound_big.play()
        

    screen = pygame.display.set_mode(constants.SCREEN_SIZE)
    

    top = Top(name = "Eye stabs.  Do you?")
    top.set_main()

    # Add the intro as a child Game to the top Game.
    intro = Intro(name ="eye stab intro")
    
    intro.loop_ogg = intro_sound_big


    top.video_intro = VideoPlayer()
    intro.games.append(top.video_intro)

    top.gig_select = GigSelect(screen.copy())
    top.games.append(top.gig_select)
    top.gig_select.stop()
    #intro = top.gig_select


    # store the player object.
    #player.player = player.Player()


    top.eyefix = EyeFixResult()
    top.games.append(top.eyefix)
    top.eyefix.stop()
    #intro = top.eyefix

    top.doctors_surgery = DoctorsSurgery(screen.copy())
    top.games.append(top.doctors_surgery)
    top.doctors_surgery.stop()



    top.games.append(intro)
    top.intro = intro

    





    note_guess = NoteGuess(name="Eye stabs.    Note Guess")

    # stop the note_guess part, because we are not ready yet.
    note_guess.stop()
    top.games.append(note_guess)
    top.note_guess = note_guess
    


    import urdpyg.sounds
    data.sounds = urdpyg.sounds.SoundManager()
    data.sounds.Load(urdpyg.sounds.SOUND_LIST, os.path.join("data", "sounds"))






    clock = pygame.time.Clock()
    clock.tick()
    
    while top.going:
        elapsed_time = clock.get_time()
        if elapsed_time:
            elapsed_time = elapsed_time / 1000.

        events = pygame.fastevent.get()

        if [e for e in events if e.type == constants.INTRO_FADEOUT]:
            intro_sound_big.fadeout(1000)
            # intro_sound_big.stop()

        # we pass in the events so all of them can get the events.
        top.handle_events(events)

        # each part that uses time, for animation or otherwise
        #   gets the same amount of elapsed time.  This also reduces the
        #   number of system calls (gettimeofday) to one per frame.
        top.update(elapsed_time)
        
        data.sounds.Update(elapsed_time)



        # the draw method retunrns a list of rects, 
        #   for where the screen needs to be updated.
        rects = top.draw(screen)

        # remove empty rects.
        rects = filter(lambda x: x != [], rects)
        #rects = filter(lambda x: type(x) not in map(type, [pygame.Rect, [], tuple([1,2])]) , rects)
        rects = filter(lambda x: type(x) not in map(type, [1]) , rects)

        # if not empty, then update the display.
        if rects != []:
            print rects
            pygame.display.update(rects)
        #pygame.display.update(rects)
        
        # we ask the clock to try and stay at a FPS rate( eg 30fps).
        #  It won't get exactly this, but it tries to get close.
        clock.tick(constants.FPS)
        #print clock.get_fps()


    # we try and clean up explicitly, and more nicely... 
    #    rather than hoping python will clean up correctly for us.
    pygame.quit()

    
    pygame.threads.quit()

    analyse_thread.quit()




