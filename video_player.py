"""

A mini video player.

"""

import os


import pygame
from pygame.locals import *

import pygame.fastevent

import rdpyg
from rdpyg.util.cyclic_list import cyclic_list

import constants

import game
Game = game.Game





class VideoPlayer(Game):


    def load(self):
        files = os.listdir( os.path.join("data", "guitar_lights") )
        files = filter(lambda x:"jpeg" in x, files)
        files.sort()

        files = cyclic_list(files)
        self.files = files


        # [(filename, surf), ...]
        self.surfs_list = []
        # [filename] = surf
        self.surfs = {}
        if 1:
            for f in files[:40]:
                s = pygame.image.load( os.path.join("data", 
                                                    "guitar_lights", 
                                                    f)).convert()
                #self.surfs_list.append( s )
                self.surfs[f] = s

        self.last_surf = None
        self.current_surf = self.surfs[ self.files[0] ]

        self.frame_up_to = self.files[0]


        self.since_start = 0.0
        self.fps = 10.0
        self.time_per_frame = 1.0 / self.fps

        self.load_at_once = 10







    def handle_events(self, events):
        Game.handle_events(self, events)

        for e in events:
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    #self.stop()
                    pass
            if e.type == constants.VIDEO_PLAYER:
                pass
                self.surfs.update(e.surf_data)

    def start_loop(self):
        pass
        # restart the frame.


    def finished(self):
        self.going = False


    def update(self, elapsed_time):
        Game.update(self, elapsed_time)

        # how many frames have past?
        # which frame?
        frame_up_to = int( self.since_start * self.fps )
        
        try:
            frame_key = self.files[frame_up_to]
        except IndexError:
            self.finished()
            return
            
        try:
            self.frame_up_to = frame_up_to

            self.last_surf = self.current_surf
            current_surf = self.surfs[frame_key]
            self.current_surf = current_surf
            
        except KeyError:
            print frame_up_to
            frame_key = None
            current_surf = None
            pass
            self.finished()
            #self.start_loop()
        
        
        if current_surf:
            self.since_start += elapsed_time
                
        
        #print "in front:%s:" % self.how_many_in_front()

        if self.how_many_in_front() < 30:
            pass
            #print "LOOOOOOOOOOOOOOOOOOOOOOOAD"
            #self.load_surfs()
            pygame.threads.tmap(lambda x: self.load_surfs(), [1], wait= False)

        self.del_old_surfs()



    def how_many_in_front(self):
        """ returns how many surfs in front we are """

        start = self.frame_up_to

        #print "start :%s:" % start
        in_front = 0
        files = self.files[start:]

        for f in self.files[start:]:
            if self.surfs.has_key(f):
                in_front += 1
            else:
                break

        return in_front
        
            
    def del_old_surfs(self):
        
        start = self.frame_up_to

        # the ones before this one.
        up_to = self.frame_up_to -1
        if up_to < 0:
            return

        files = self.files[:up_to]

        for f in files:
            if self.surfs.has_key(f):
                del self.surfs[f]

        

    def load_surfs(self):
        #print "loading surfs!!!"

        start = self.frame_up_to + self.how_many_in_front()
        end = self.load_at_once + start

        files = self.files[start:end]

        #print files

        surfs = {}
        for f in files:
            s = pygame.image.load( os.path.join("data", 
                                                "guitar_lights", 
                                                f)).convert()
            surfs[f] = s


        pygame.fastevent.post (
            pygame.event.Event(constants.VIDEO_PLAYER, surf_data = surfs)
        )




    def draw(self, screen):
        rects = Game.draw(self, screen)

        #screen.fill((0,0,0,255))


        if self.last_surf != self.current_surf:
            r = screen.blit(self.current_surf, (0,0))
            rects.append(r)
        # update the whole screen.
        #rects.extend(screen.get_rect())

        return rects







    def play(self):
        """ starts playing it.
        """

        # which frame are we up to?




