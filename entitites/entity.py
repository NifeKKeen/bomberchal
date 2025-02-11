import pygame


class Entity(pygame.sprite.Sprite):
    Id = 0


    def __init__(self, **kwargs):
        super().__init__()

        self.x = kwargs.get("x", 0)  # position x in board (from left) [целые коорды]
        self.y = kwargs.get("y", 0)  # position x in board (from top) [целые коорды]
        self.px_x = kwargs.get("px_x", 0)  # position x in pixels (from left) [пиксельные коорды]
        self.px_y = kwargs.get("px_y", 0)  # position y in pixels (from top) [пиксельные коорды]
        self.px_w = kwargs.get("px_w", 1)  # width in pixels
        self.px_h = kwargs.get("px_h", 1)  # height in pixels

        self.id = Entity.Id
        Entity.Id += 1

        self.tick = 0  # lifespan

        self.displayed = False  # is interactable and visible in screen

        self.image = pygame.Surface([self.px_w, self.px_h])  # IMPORTANT!
        # self.image.fill((0, 0, 255))  # if there are no image
        self.image.set_colorkey((0, 0, 0))  # color to make transparent

        pygame.draw.rect(self.image, (255, 255, 255), pygame.Rect((0, 0, self.px_w, self.px_h)))

        self.rect = self.image.get_rect()
        self.rect.x = self.px_x
        self.rect.y = self.px_y

    def move_px(self, x = 0, y = 0):
        self.rect.x += x
        self.px_x += x

        self.rect.y += y
        self.px_y += y


    def disable(self):
        self.displayed = False


    def enable(self):
        self.displayed = True
