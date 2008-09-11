from pygame.locals import *
import pygame

from game import Game
import songs

import constants
import data

# Show notes on the screen, and people have to tap keyboard in time with notes.

# notes_time = [["a", 0.0+s], ["c", 2.0+s], ["b", 4.0+s], ["c", 7.0+s], ]


# how do we do sharps/flats on a computer keyboard?
NOTES = u"abcdefg"

class NoteGuess(Game):
    """ Notes are presented to the person... 
            and they have to guess what they are.
    """

    def load(self):
        self.notes_to_press = []
        
        # [[note, elapsed_time], ...]
        self.notes_time = []
        
        self.elapsed_time = 0.0
        
        
        # total time allowed in the song.
        self.total_time = 30.

        self.font_size = 40
        self.font = pygame.font.Font(data.filepath("freesansbold.ttf"), self.font_size)
        self.font_color = (255,255,255,255)
        self.font_color = (0,0,0,255)

        # the song currently being played.
        self.current_song = songs.Song()

        # a dummy song.

        s = 2.0
        self.current_song.notes_time = [["a", 0.0+s], ["c", 2.0+s], ["b", 4.0+s], ["c", 7.0+s], ]

    def draw(self, screen):
        """
                - from [[note,time], ...] 
                - display notes across the screen.   
                    - total time, eg 30.0 seconds - divided by screen width (640)
                        - draw a note at the pos, or an underline.

                - display position of time.  As a line from top of screen to bottom.
        """
        rects = []

        if self.notes_time:
            # the notes that people press.
            print self.notes_time


        screen.fill((255, 255, 255,255))
        
        
        # draw the representation of time.  
        #     A line from top to bottom of screen, that moves.

        self.screen_width = screen.get_width()
        time_line_x = self.get_position_for_time(self.elapsed_time)

        pygame.draw.line(screen, 
                         (255,0,0,255), (time_line_x, 0), 
                         (time_line_x, screen.get_height()), 1)


        # draw the position of played notes time
        text_y = screen.get_rect().center[1]
        self.draw_notes_time(self.notes_time, text_y, screen)


        # draw the notes we need to play.
        self.draw_notes_time(self.current_song.notes_time, text_y + 50, screen, 
                             draw_allowed = True, allowed_time = 0.3)


        # clear the notes that we've processed.
        #self.notes_time = []


        # update the whole screen.
        rects.append( screen.get_rect() )
        return rects


    def draw_notes_time(self, notes_time, text_y, screen, draw_allowed = False, allowed_time = 0.3):
        rects = []

        for n,t in notes_time:

            # the left of the letter is where it is.  
            #    Should it be the center of the letter?
            text_x = self.get_position_for_time(t)


            the_text = self.font.render(n, 1, self.font_color)

            text_blit_r = screen.blit(the_text, (text_x,text_y))
            rects.append(text_blit_r)

            line_color = (0,0,255,255)
            r = pygame.draw.line(screen, 
                                 line_color, (text_x, text_blit_r.bottom), 
                                 (text_x, text_blit_r.bottom - 5), 1)
            rects.append(r)


            # draw the line on each side of the note... allowed time.

            note_left = self.get_position_for_time(t - allowed_time)
            note_right = self.get_position_for_time(t + allowed_time)


            if draw_allowed:
                line_color = (0,255,0,255)
                r = pygame.draw.line(screen, 
                                     line_color, (note_left, text_blit_r.bottom+5), 
                                     (note_left, text_blit_r.bottom - 5), 2)
                rects.append(r)
                r = pygame.draw.line(screen, 
                                     line_color, (note_right, text_blit_r.bottom+5), 
                                     (note_right, text_blit_r.bottom - 5), 2)
                rects.append(r)






        return rects



    def get_position_for_time(self, some_time):
        """ given some time, return the position on the screen for
              that time.
        """
        time_line_x = some_time * (self.screen_width / self.total_time)

        return time_line_x
        

    def handle_events(self, events):
        Game.handle_events(self, events)

        notes_pressed = []

        for e in events:
            if e.type == KEYDOWN:
                
                if e.unicode in NOTES: 
                    print "HIIH!!"
                    notes_pressed.append(e.unicode)

            if e.type == constants.PITCH_DETECT:
                notes_pressed.append(e.note)

        self.notes_last_pressed = notes_pressed

    def update_notes(self, elapsed_time):
        # translate the notes into [[note, elapsed_time], ]
        all_notes = []
        for note in self.notes_last_pressed:
            all_notes.append( [note, elapsed_time] )

        self.notes_last_pressed = []

        self.notes_time.extend(all_notes)


    def update(self, elapsed_time):
        Game.update(self, elapsed_time)

        # process any input notes 
        self.update_notes(self.elapsed_time)
