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
import timing

from constants import *

################################################################################
# These values will probably need to be tweaked for each guitar

# note must be at least this to be counted
MINIMUM_VOLUME     = -20

# The range is 0dB for the maximally loud sounds down to -40dB for silence.
# Typical very loud sounds are -1dB and typical silence is -36dB.

# note must be X louder than previous to count as new note
ATTACK_DELTA       =  2

# X midi notes
OCTAVE_CORRECTION  =  12

SAMPLE_SIZE        =  1024

################################################################################

class PitchDectectThread(threading.Thread):
    def __init__(self, *args, **kw):
        threading.Thread.__init__(self)
        self._args = args
        self._kw = kw

    def init_audio(self):
        # XXX SHOULD THIS BE MOVED OUT? pyaud reference passed in at __init__?
        pyaud = pyaudio.PyAudio()

        self.stream = pyaud.open ( *self._args, **self._kw )

    def post_note(self, note, t, d, v):
        for _ in range(5):
            try:
                pygame.fastevent.post (
                    event.Event (
                        PITCH_DETECT, 
                        note = note,
                        time = t, 
                        delta = d,
                        volume = v,
                    )
                )
                break
            except Exception, e:
                pass

    def run(self):
        self.init_audio()

        last_note = last_vol = last_time = 0

        while True:
            # Read raw data
            rawsamps = self.stream.read(SAMPLE_SIZE)
            t = timing.get_time()

            # Convert raw data to NumPy array
            samps = numpy.fromstring(rawsamps, dtype=numpy.int16)
            
            midi_note = analyse.musical_detect_pitch(samps, min_note=25.0)
        
            if midi_note:
                midi_note += OCTAVE_CORRECTION
            
                latest_note = notes.midi_to_note(midi_note)        
                latest_vol = analyse.loudness(samps)
                
                attacked = latest_vol - last_vol > ATTACK_DELTA
                
                if latest_note != last_note or attacked:
                    if latest_vol > MINIMUM_VOLUME:
                        self.post_note(latest_note, t, t - last_time, latest_vol)

                    last_note = latest_note
                    last_vol = latest_vol
                    last_time = t
            
            elif last_note:
                last_note = None

################################################################################

def example():
    pygame.init()
    pygame.fastevent.init()

    t = PitchDectectThread (
        format = pyaudio.paInt16,
        channels = 2,
        rate = 44100,
        input_device_index = 1,
        input = True 
    )

    t.setDaemon(1)
    t.start()

    while True:
        events = pygame.fastevent.get()
        for e in events:
            print e

################################################################################

if __name__ == '__main__':
    example()

################################################################################