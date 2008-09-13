"""

A mini video player.

"""

import os


import pygame
from pygame.locals import *

import pygame.fastevent

import rdpyg
from rdpyg.util.cyclic_list import cyclic_list

import constant

import game
Game = game.Game


class VideoPlayer(Game):


    def load(self):
        files = os.listdir( os.path.join("data", "guitar_lights") )
        files = filter(lambda x:"jpeg" in x, files)
        files.sort()

        files = cyclic_list(files)




    def handle_events(self, events):
        Game.handle_events(self, events)

        for e in events:
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    #self.stop()
                    pass
            if e.type == constants.VIDEO_PLAYER:
                pass
                self.surfs.append()



    def update(self, elapsed_time):
        Game.update(self, elapsed_time)


    def draw(self, screen):
        rects = Game.draw(self, screen)

        screen.fill((0,0,0,255))


        # update the whole screen.
        rects.extend(screen.get_rect())

        return rects

    def post_event(self, event):
        pygame.fastevent.post()


    def play(self):
        """ starts playing it.
        """

        # which frame are we up to?



    def stop(self):
        """
        """













