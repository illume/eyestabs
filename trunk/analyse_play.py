################################################################################
# STD LIBS

import sys

# 3RD PARTY LIBS

import numpy
import pyaudio
import analyse

# USER LIBS

import notes
import timing

from constants import *

################################################################################
# These values will probably need to be tweaked for each guitar

# note must be at least this to be counted
# The higher the less chance "noise" will be detected as notes but means notes
# must be played hard

MINIMUM_VOLUME     = -15

# The range is 0dB for the maximally loud sounds down to -40dB for silence.
# Typical very loud sounds are -1dB and typical silence is -36dB.

# note must be X decibels louder than previous to count as new note
ATTACK_THRESHOLD       =  2

# X midi notes, semitones
OCTAVE_CORRECTION  =  12

# Analyse X samples at a time
SAMPLE_SIZE        =  1024

################################################################################

def main():
    pyaud = pyaudio.PyAudio()
    
    stream = pyaud.open (
        format = pyaudio.paInt16,
        channels = 2,
        rate = 44100,
        input_device_index = 1,
        input = True 
    )
    
    last_note = last_vol = last_time = 0
    
    volumes = []
    
    log = open('fuck.txt', 'a')
        
    while True:
        # Read raw data
        rawsamps = stream.read(SAMPLE_SIZE)
        t = stream.get_time()
    
        # Convert raw data to NumPy array
        samps = numpy.fromstring(rawsamps, dtype=numpy.int16)
    
        midi_note = analyse.musical_detect_pitch(samps, min_note=28.0)

        if midi_note:
            midi_note += OCTAVE_CORRECTION
    
            latest_note = notes.midi_to_note(midi_note)       
            latest_vol = analyse.loudness(samps)
    
            attacked = latest_vol - last_vol > ATTACK_THRESHOLD
    
            if latest_note != last_note or attacked:
                if latest_vol > MINIMUM_VOLUME:
                    delta = t - last_time

                    print repr({'note':latest_note, 'time': t})
                    sys.stdout.flush()

                    last_time = t

                last_note = latest_note
                last_vol = latest_vol
    
        elif last_note:
            last_note = None

            print repr({'note':'nothing', 'time': t})
            sys.stdout.flush()

if __name__ == '__main__':
    main()
