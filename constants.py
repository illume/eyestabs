import pygame

PITCH_DETECT         = pygame.USEREVENT + 10
VIDEO_PLAYER         = pygame.USEREVENT + 11


FPS = 30
SCREEN_SIZE = (640,480)


# how much time do they have to get a note?
TIME_MS_TO_GET_NOTE = 200


# other constants can go here!   yes indeed...
INTRO_FADEOUT = pygame.USEREVENT + 2