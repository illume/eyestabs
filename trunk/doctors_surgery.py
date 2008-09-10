"""

The doctors surgery part of the game.

"""

import pygame
from pygame.locals import *

import game
Game = game.Game


class DoctorsSurgery(Game):


    def handle_events(self, events):
        Game.handle_events(self, events)

        for e in events:
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    #self.stop()
                    pass


    def update(self, elapsed_time):
        Game.update(self, elapsed_time)


    def draw(self, screen):
        rects = Game.draw(self, screen)

        screen.fill((0,0,0,255))


        # update the whole screen.
        rects.extend(screen.get_rect())

        return rects



















