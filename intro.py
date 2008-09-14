
import pygame
from pygame.locals import *

import game
Game = game.Game

import data
import textwrap


class Intro(Game):
    def load(self):
        Game.load(self)
        self.font_size = 40
        self.font = pygame.font.Font(data.filepath("freesansbold.ttf"), self.font_size)
        self.font_color = (255,255,255,255)

        # should we be drawing the line element of the intro?
        self.draw_lines = 0

        self.second_text = 0

        self.first_text = 1


    def handle_events(self, events):
        Game.handle_events(self, events)

        for e in events:
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    self.stop()
                if e.key == K_s:
                    pass
                    #pygame.image.save(pygame.display.get_surface(), "eye_stab_screeny_2008_09_09.png")
                    
        
    def update(self, elapsed_time):
        Game.update(self, elapsed_time)

        print 'updating...'

        if self.elapsed_time < 2.0:
            self.text_string = "Eye stabs.   Do you?"
        elif self.elapsed_time >= 2.0 and self.elapsed_time < 4.0:
            self.text_string = "Yeah I do stabs."
            self.draw_lines = 1
          
        elif self.elapsed_time >= 4.0 and self.elapsed_time < 8.0:
            self.text_string = "Cool.  I like you then."

        elif self.elapsed_time >= 8.0 and self.elapsed_time < 24.0:
            pass


        elif self.elapsed_time >= 24.0 and self.elapsed_time < 800.0:

            self.second_text = 1
            self.first_text = 0
            self.draw_lines = 0

            print 'doit...'



        elif self.elapsed_time >= 900.0 and self.elapsed_time < 1000.0:
            #self.stop()
            data.where_to = "gig_select"




    def draw(self, screen):
        rects = Game.draw(self, screen)





        if self.first_text:


            the_text = self.font.render(self.text_string, 1, self.font_color)

            #screen.fill((0,0,0,255))

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


        if self.second_text:

            intro_text = """
<SCARY DARK SILLY VOICE OVER VOICE>
In the dirty underground music scene often referred to as 'eye stabs', there are lethal gigs in select nightclubs around the world.  Musicians play for eyes. A tune is played to the musician, and they must figure out the notes played.

Fuck up the tune, and you are stabbed in the eye! Get the tune right, then fortune and respect are yours! Better than the riches and the adoration though -- rich club owners can give you spare eyes... and provide doctors that can give you back eyes you have had stabbed out.

So are you prepared to put your eyes on the line? Can you play well enough to avoid a stab in the eye? Do you trust the sleazy club owners doctors to fix your eye if it does get stabbed? 

</SCARY DARK SILLY VOICE OVER VOICE>
            """

            #print self.elapsed_time

            text_lines = textwrap.wrapline(intro_text, self.font, 630)
            print text_lines
            new_lines = []
            for l in text_lines:
                new_lines.extend( l.split("\n") )

            text_lines = new_lines
            
            screen.fill((237, 99, 127))


            for i, text_string in enumerate(text_lines):
                the_text = self.font.render(text_string, 1, self.font_color)

                # draw the text in the middle of the screen.
                text_x = 5
                start_time = 25.
                time_speed = (self.elapsed_time - start_time) * 14
                #print time_speed
                text_y = ((the_text.get_height() * 1.2 *  i) - time_speed)
                #print text_y

                if text_y + the_text.get_height() < screen.get_height():
                    if text_y + the_text.get_height() > 0:

                        r = screen.blit(the_text, (text_x,text_y))







        # update the whole screen.
        rects.extend(screen.get_rect())

        return rects




    def stop(self):
        """
        """
        print 'intro stopped'
        self.going = False

        data.where_to = "gig_select"




