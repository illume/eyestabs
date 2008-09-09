################################################################################
# STD LIBS

import threading
import time

# 3RD PARTY LIBS

import numpy
import pyaudio
import analyse

import pygame
import pygame.event as event

# USER LIBS

import notes

################################################################################

# note must be at least this to be counted
MINIMUM_VOLUME     = -18

# note must be X louder than previous to count as new note
ATTACK_DELTA       =  4

# X midi notes
OCTAVE_CORRECTION  =  12   

NOTE_EVENT         = pygame.USEREVENT + 20

################################################################################

class PitchDectectThread(threading.Thread):
    def init_audio(self):
        #### THIS WILL BE MOVED --- PARAMETERIZED FROM __init__
        
        # Initialize PyAudio
        pyaud = pyaudio.PyAudio()

        # Open input stream, 16-bit mono at 44100 Hz
        # On my system, device 2 is a USB microphone, your number may differ.
        self.stream = pyaud.open (
            format = pyaudio.paInt16,
            channels = 2,
            rate = 44100,
            input_device_index = 1,
            input = True )

    def post_note(self, note):
        print note
        
        for t in range(5):
            try:
                pygame.fastevent.post(event.Event(NOTE_EVENT, note=note))
                print 'event posted'
                break
            except Exception, e:
                print 'fail'
                
    def run(self):
        self.init_audio()

        last_note = last_vol = 0

        while True:
            # Read raw data
            rawsamps = self.stream.read(1024)
            # Convert raw data to NumPy array
            samps = numpy.fromstring(rawsamps, dtype=numpy.int16)
            
            midi_note = analyse.musical_detect_pitch(samps, min_note=25.0)
        
            if midi_note is None and last_note:
                last_note = None
        
            if midi_note:
                midi_note += OCTAVE_CORRECTION
            
                latest_note = notes.midi_to_note(midi_note)        
                latest_vol = analyse.loudness(samps)
                
                attacked = latest_vol - last_vol > ATTACK_DELTA
                
                if latest_note != last_note or attacked:
                    if latest_vol > MINIMUM_VOLUME:
                        self.post_note(latest_note)

                    last_note = latest_note
                    last_vol = latest_vol
            
################################################################################

if __name__ == '__main__':
    pygame.init()
    pygame.fastevent.init()
    
    t = PitchDectectThread()
    t.setDaemon(1)
    t.start()

    while True:
        events = pygame.fastevent.get()
        for e in events:
            print e

################################################################################