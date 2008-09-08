import numpy
import pyaudio
import analyse

import notes

import os

# Initialize PyAudio
pyaud = pyaudio.PyAudio()

# Open input stream, 16-bit mono at 44100 Hz
# On my system, device 2 is a USB microphone, your number may differ.
stream = pyaud.open(
    format = pyaudio.paInt16,
    channels = 2,
    rate = 44100,
    input_device_index = 1,
    input = True)

mapping = notes.pitch_mapping()

last_note = None
last_vol = 0

while True:
    # Read raw microphone data
    rawsamps = stream.read(1024)
    # Convert raw data to NumPy array
    samps = numpy.fromstring(rawsamps, dtype=numpy.int16)
    # Show the volume and pitch
    # analyse.loudness(samps), 
    
    #  detect_pitch(chunk, min_frequency=82.0, max_frequency=1000.0, samplerate=441
    # 0, sens=0.1, ratio=5.0):
    
    pitch = analyse.detect_pitch(
        samps, 
        min_frequency=40,
        sens=0.1,
    )

    if pitch is None and last_note:
        last_note = None

    if pitch:
        latest_note = notes.closest_note(mapping, (pitch or -1) * 2)
        latest_vol = analyse.loudness(samps)
        
        if 'E1' in latest_note:
            os.system('cls')
        
        if latest_note != last_note or latest_vol - last_vol > 3:
            if analyse.loudness(samps) > - 15:
                print latest_note[1]
            
            
            
            last_note = latest_note
            last_vol = latest_vol