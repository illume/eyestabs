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
        
    def draw(self, screen):
        """
	"""
	return rects
        
        
        
    def handle_events(self, events):
        Game.handle_events(self, events)

	notes_pressed = []

	for e in events:
	    if e.type == KEYDOWN:
	        if e.unicode in NOTES: 
		    notes_pressed.append(e.unicode)

        self.notes_last_pressed = notes_pressed


    def notes(self, notes_pressed):
        self.notes_to_press.append( notes_pressed )


    def update_notes(self, elapsed_time):
        # translate the notes into [[note, elapsed_time], ]
        all_notes = []
	for note_set in self.notes_to_press:
	    for note in note_set:
                all_notes.append( [note, elapsed_time] )

        self.notes_to_press = []

	self.notes_time.extend(all_notes)


    def update(self, elapsed_time):
        Game.update(self, elapsed_time)

	# process any input notes 
	self.update_notes(self.elapsed_time)





