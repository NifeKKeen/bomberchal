import pygame, sys
from pygame.locals import *
import paint_api
from entitites.entity import Entity
from pages import menu

# GLOBAL VARIABLES START

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Bomberchal")

Frame = pygame.time.Clock()
FPS = 60
all_sprites = pygame.sprite.Group()

# GLOBAL VARIABLES END

if __name__ == "__main__":
    pygame.init()

    while True:
        # menu()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        DISPLAYSURF.fill((20, 20, 50))

        # all_sprites.update()
        all_sprites.draw(DISPLAYSURF)
        pygame.display.flip()

        Frame.tick(FPS)
