################################################################################
# STD LIBS

import sys
import random
import time

# 3RD PARTY LIBS
import pygame

from ocempgui.widgets import *
from ocempgui.widgets.Constants import *

import numpy
import pyaudio
import analyse

# USER LIBS

import notes
import timing

from constants import *

################################################################################

def _update_parameter(scale, label, norm=None):
    if norm:     scale.value = norm(scale.value)
    label.text = label.format % scale.value

class _Paramaters(Table):
    _paramaters = 0
    
    def add_paramater(self, name, low, hi, start_val=0, norm=None):
        format = name + ": %f"
        
        scale = HScale(low, hi)
        scale.value = start_val

        label = Label (format % scale.value)
        label.format = format

        scale.connect_signal (
            SIG_VALCHANGED, _update_parameter, scale, label, norm
        )

        self.add_child(self._paramaters , 0, scale)
        self.add_child(self._paramaters + 1, 0, label)

        self._paramaters += 2

        prop = property(lambda self: scale.value)
        setattr(_Paramaters, name, prop)

################################################################################

def Paramaters(*params):
    paramaters = _Paramaters(len(params)*2, 1)
    paramaters.topleft = 5, 5
    paramaters.spacing = 5

    for param in params: paramaters.add_paramater(*param)

    return paramaters

################################################################################

paramaters = Paramaters (
    ("minimum_volume",      -22,    -8,    -17),

    ("attack_threshold",     0,     5,     2),

    ("octave_correction",    -2,     2,     1,       int),

    ("sample_size",          512,   4096,  1024,   lambda s: int((s//256)*256)),
)

################################################################################

# Initialize pygame window
pygame.init ()
screen = pygame.display.set_mode ((200, 250));
screen.fill ((234, 228, 223))

# Create the Renderer to use for the UI elements.
re = Renderer ()

# Bind it to a part of the screen, which it will use to draw the widgets.
# Here we use the complete screen.
re.screen = screen

re.add_widget (paramaters)

################################################################################

pyaud = pyaudio.PyAudio()

stream = pyaud.open (
    format = pyaudio.paInt16,
    channels = 2,
    rate = 44100,
    input_device_index = 1,
    input = True 
)

################################################################################

last_note = last_vol = last_time = 0

################################################################################

while True:
    events = pygame.event.get ()
    for ev in events:
        if ev.type == pygame.QUIT:
            sys.exit ()
    
    if events:
        re.distribute_events (*events)
        re.refresh ()

    t = timing.get_time()
    
    available = stream.get_read_available()
    sample_size = int(paramaters.sample_size)
    if not available > sample_size:
        time.sleep(0.01)
        continue

    rawsamps = stream.read(available)
    samps = numpy.fromstring(rawsamps, dtype=numpy.int16, count=sample_size)

    event = ''
    
    midi_note = analyse.musical_detect_pitch(samps, min_note=28.0)
    
    if midi_note:
        midi_note += paramaters.octave_correction * 12

        latest_note = notes.midi_to_note(midi_note)
        latest_vol = analyse.loudness(samps)

        attacked = latest_vol - last_vol > paramaters.attack_threshold

        if latest_note != last_note or attacked:
            if latest_vol > paramaters.minimum_volume:
                event = {'note':     latest_note,    'time':     t}
                last_time = t

            last_note = latest_note
            last_vol = latest_vol

    elif last_note:
        last_note = None

    print event
    sys.stdout.flush()

################################################################################