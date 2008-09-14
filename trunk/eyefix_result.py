"""

The doctors surgery part of the game.

"""
import os, random


import pygame
from pygame.locals import *

import data, constants
import game
Game = game.Game

class EyeFixResult(Game):


    def load(self):

        self.background = pygame.image.load(os.path.join("data", "images", "doctor_yellow2.jpg"))


        self.font_size = 40
        self.font = pygame.font.Font(data.filepath("freesansbold.ttf"), self.font_size)
        self.font_color = (255,255,255,255)

        self.text_string = [""]


    def choose_result(self):
        """
        """
        r = random.choice([(1, ["I fixed your eye!"]), 
                           (0, ["Oh noes!!!  I seem to have",  "just made the wound worse!"])])
        self.text_string = r[1] + ["    press enter..."]

    def handle_events(self, events):
        Game.handle_events(self, events)

        for e in events:
            if e.type == KEYDOWN:
                #if e.key == K_ESCAPE:
                #    self.stop()
                #    break
                #    pass
                data.where_to = "gig_select"
                #self.stop()


    def update(self, elapsed_time):
        Game.update(self, elapsed_time)


    def draw(self, screen):
        rects = Game.draw(self, screen)

        screen.blit(self.background, (0,0))

        for i, text_string in enumerate(self.text_string):
            the_text = self.font.render(text_string, 1, self.font_color)

            # draw the text in the middle of the screen.
            x,text_y = screen.get_rect().center
            text_x = x - (the_text.get_width() / 2)
            text_y += (the_text.get_height() * 1.2 *  i)

            r = screen.blit(the_text, (text_x,text_y))




        # update the whole screen.
        rects.extend([screen.get_rect()])

        return rects








