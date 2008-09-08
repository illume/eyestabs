from pygame.locals import *
import pygame
from game import Game


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
	


    def draw(self, screen):
        """
	"""

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


        time_line_x = self.elapsed_time * (screen.get_width() / self.total_time)
	
	pygame.draw.line(screen, 
	                 (255,0,0,255), (time_line_x, 0), 
	                 (time_line_x, screen.get_height()), 1)


        #TODO: draw the position of notes time



        # clear the notes that we've processed.
	#self.notes_time = []

        # update the whole screen.
	rects.append( screen.get_rect() )
	return rects
        
        
        
    def handle_events(self, events):
        Game.handle_events(self, events)

	notes_pressed = []

	for e in events:
	    if e.type == KEYDOWN:
	        
	        if e.unicode in NOTES: 
		    print "HIIH!!"
		    notes_pressed.append(e.unicode)

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





