################################################################################

import math

################################################################################

INTERVALS = [
    'Perfect unison',
    'Minor second',
    'Major second',
    'Minor third',
    'Major third',
    'Perfect fourth',
    'Tritone',
    'Perfect fifth',
    'Minor sixth',
    'Major sixth',
    'Minor seventh',
    'Major seventh',
    'Perfect octave',
]

MAJOR_SCALE = [0, 2, 4, 5, 7, 9, 11]

NOTES = [
    'C',
    'C#',
    'D',
    'D#',
    'E',
    'F',
    'F#',
    'G',
    'G#',
    'A',
    'A#',
    'B'
]

MODES = [
    'Ionian', 
    'Dorian', 
    'Phrygian', 
    'Lydian', 
    'Mixolydian', 
    'Aeolian',
    'Locrian'
]

################################################################################

def scale(start):
    pos = NOTES.index(start)
    return NOTES[pos:] + NOTES[:pos]

def major_scale(start):
    key = scale(start)
    return [key[p] for p in MAJOR_SCALE]

def interval(first, second):
    first_scale = scale(first)
    return INTERVALS[first_scale.index(second)]

def mode(start, which_mode):
    major = major_scale(start)
    pos = MODES.index(which_mode)
    return major[pos:] + major[:pos]

################################################################################

def pitch_mapping():
    degree = math.pow(2, 1/12.0)

    e_scale = scale('E')

    start_frequency = 55 * math.pow(degree, 7)
    semitones = range(49)   # 4 Octaves,

    return [
        (
            start_frequency * math.pow(degree, i),
            e_scale[i%12] + str(i/12 + 1)
        )
        for i in semitones
    ]

def closest_note(mapping, search):
    return min(mapping, key=lambda i: abs(search - i[0]))

def main():
    mapping = pitch_mapping()
    print closest_note(mapping, 123)
    
################################################################################

if __name__ == '__main__':
    main()

################################################################################