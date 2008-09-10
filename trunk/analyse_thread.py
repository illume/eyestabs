################################################################################
# STD LIBS

import threading
import time
import sys
import subprocess

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

class PitchDectectThread(threading.Thread):
    def __init__(self, *args, **kw):
        threading.Thread.__init__(self)
        self._args = args
        self._kw = kw

        self.running = True

    def post_note(self, attributes):
        if attributes['note'] == "nothing":
            return
        for _ in range(5):
            try:
                pygame.fastevent.post (
                    event.Event ( PITCH_DETECT, **attributes)
                )
                break
            except Exception, e:
                pass

    def run(self):
        print 'thread started'

        cmd = [sys.executable, 'analyse_play.py']

        proc = subprocess.Popen ( cmd, 
            stdout = subprocess.PIPE,  universal_newlines = 1,
            stderr = subprocess.PIPE,  stdin=subprocess.PIPE
        )

        ret_code = None
        response = []

        while ret_code is None:
            print 'asdf 1'
            ret_code = proc.poll()
            print 'asdf 2'
            self.post_note(eval(proc.stdout.readline().strip()))

        print 'thread ended'

################################################################################

def init():
    t = PitchDectectThread()
    t.setDaemon(1)
    t.start()

def example():
    pygame.init()
    pygame.fastevent.init()

    init()

    while True:
        events = pygame.fastevent.get()
        for e in events:            
            print e

################################################################################

if __name__ == '__main__':
    example()

################################################################################
