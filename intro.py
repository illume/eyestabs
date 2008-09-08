
import pygame
from pygame.locals import *

import game
Game = game.Game



class Intro(Game):
    def load(self):
        Game.load(self)
        self.font_size = 40
        self.font = pygame.font.Font(None, self.font_size)
        self.font_color = (255,255,255,255)

        self.draw_lines = 0

    def handle_events(self, events):
        Game.handle_events(self, events)

        for e in events:
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    self.stop()
        
    def update(self, elapsed_time):
        Game.update(self, elapsed_time)

        if self.elapsed_time < 2.0:
            self.text_string = "Eye stabs.   Do you?"
        elif self.elapsed_time >= 2.0 and self.elapsed_time < 4.0:
            self.text_string = "Yeah I do stabs."
            self.draw_lines = 1
          
        elif self.elapsed_time >= 4.0 and self.elapsed_time < 8.0:
            self.text_string = "Cool.  I like you then."

        elif self.elapsed_time >= 8.0 and self.elapsed_time < 20.0:
            pass
        elif self.elapsed_time >= 10.0 and self.elapsed_time < 800.0:
            self.stop()



    def stop(self):
        """
        """
        print 'intro stopped'
        self.going = False

    def draw(self, screen):
        rects = Game.draw(self, screen)
        the_text = self.font.render(self.text_string, 1, self.font_color)

        screen.fill((0,0,0,255))

	# draw the text in the middle of the screen.
        x,text_y = screen.get_rect().center
        text_x = x - (the_text.get_width() / 2)

        r = screen.blit(the_text, (text_x,text_y))



	# how fast the notes move.  difference in x.
	note_dxes = [5,8,10,3,6,12]

        if self.draw_lines:
	    # lines (guitar strings) go down the screen.
	    #    Some notes move across each of the strings at different speeds.
            
            for mult, note_dx in zip(range(20,26), note_dxes):
                y = int(self.elapsed_time * mult)
                pygame.draw.line(screen, (255,255,255,255), (0,y), (screen.get_width()-1, y), 5)

		# draw the notes going along the string lines.
		note_x = note_dx * self.elapsed_time * 3
                pygame.draw.line(screen, (255,0,0,255), (note_x,y+5), (note_x, y-5), 4)




        # update the whole screen.
        rects.extend(screen.get_rect())

        return rects








