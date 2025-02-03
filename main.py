import sys
import pygame
from pygame.locals import *

pygame.init()
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

FPS = pygame.time.Clock()
FPS.tick(60)

while True:
  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
      sys.exit()
  
  pygame.display.update()
