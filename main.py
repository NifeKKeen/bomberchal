import sys
import pygame
import menu

from pygame.locals import *

pygame.init()
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

FPS = pygame.time.Clock()
FPS.tick(60)

menu()
