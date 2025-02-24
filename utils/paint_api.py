import pygame

import globals
from utils.helpers import rand


def format_surface_id_to_key(surface_id):
    return "sid_" + str(surface_id)


class SurfaceSprite(pygame.sprite.Sprite):
    SurfaceId = 0

    def __init__(self, **kwargs):
        super().__init__()

        self.px_x = kwargs.get("px_x", 0)  # position x in pixels (from left) [пиксельные коорды]
        self.px_y = kwargs.get("px_y", 0)  # position y in pixels (from top) [пиксельные коорды]
        self.px_w = kwargs.get("px_w", 1)  # width in pixels
        self.px_h = kwargs.get("px_h", 1)  # height in pixels

        self.color = kwargs.get("color", (rand(128, 256), 0, rand(128, 256)))
        self.layer = kwargs.get("layer", 0)  # Like z-index in CSS

        self.surface_id = SurfaceSprite.SurfaceId
        self.key = kwargs.get("key", format_surface_id_to_key(self.surface_id))
        SurfaceSprite.SurfaceId += 1

        self.mounted = False  # is visible in screen

        self.image_path = kwargs.get("image_path", None)

        if kwargs.get("should_init_surface", True):
            self.__init_surface__()

    def __init_surface__(self):
        if self.image_path is not None:
            self.image = pygame.transform.scale(pygame.image.load(self.image_path).convert_alpha(), (self.px_w, self.px_h))
        else:
            self.image = pygame.Surface([self.px_w, self.px_h])  # IMPORTANT!
            self.image.set_colorkey((0, 0, 0))  # color to make transparent
            self.image.fill(self.color)  # Color of surface
            pygame.draw.rect(self.image, self.color, pygame.Rect((0, 0, self.px_w, self.px_h)))

        self.rect = self.image.get_rect()
        self.rect.x = self.px_x
        self.rect.y = self.px_y

    def unmount(self):
        self.mounted = False
        unmount_sprite(self)


    def mount(self):
        self.mounted = True
        mount_sprite(self)

    def move_px(self, x=0, y=0):
        self.px_x += x
        self.px_y += y
        self.rect.x += x
        self.rect.y += y

    def set_px(self, x=0, y=0):
        self.px_x = x
        self.px_y = y
        self.rect.x = x
        self.rect.y = y

    def collides_with(self, sprite2):
        return self.mounted and sprite2.mounted and pygame.sprite.collide_rect(self, sprite2)

class TextSprite(SurfaceSprite):
    def __init__(self, **kwargs):
        super().__init__(**kwargs, should_init_surface=False)
        self.font_size = kwargs.get("key", None)
        self.color = kwargs.get("color", (0, 0, 0))
        self.font_size = kwargs.get("font_size", 14)
        self.font = kwargs.get("font_family", None)
        self.text = kwargs.get("text", "-")
        self.align = kwargs.get("align", "topleft")

        self.font_obj = pygame.font.Font(self.font, self.font_size)

        if kwargs.get("should_init_surface", True):
            self.__init_surface__()

    def __init_surface__(self):
        self.image = self.font_obj.render(self.text, True, self.color)
        self.rect = self.image.get_rect()

        self.rect.__setattr__(self.align, (self.px_x, self.px_y))



def _get_surface(**kwargs):
    # if surface_id is not specified, generate a new surface with its unique id
    # otherwise, try to get surface from globals.map_key_sprite with this surface_id
    surface_key = kwargs.get("key", None)

    if surface_key not in globals.to_render_keys:
        surface_sprite = SurfaceSprite(**kwargs)
        print("Rendered", surface_sprite.key)
    else:
        surface_sprite = globals.map_key_sprite[surface_key]

    return surface_sprite


def _get_text_surface(**kwargs):
    # if surface_id is not specified, generate a new surface with its unique id
    # otherwise, try to get surface from globals.map_key_sprite with this surface_id
    surface_key = kwargs.get("key", None)

    if surface_key not in globals.to_render_keys:
        surface_sprite = TextSprite(**kwargs)
        print("Rendered", surface_sprite.key)
    else:
        surface_sprite = globals.map_key_sprite[surface_key]

    return surface_sprite


def mount_rect(**kwargs):
    # key should be specified in order to decrease the number of renders
    # otherwise a new surface will be created and rendered each frame

    sprite = _get_surface(**kwargs)
    sprite.mounted = True

    globals.all_sprites.add(sprite)
    globals.map_key_sprite[sprite.key] = sprite
    globals.to_render_keys.add(sprite.key)

    return sprite


def mount_text(**kwargs):
    # key should be specified in order to decrease the number of renders
    # otherwise a new surface will be created and rendered each frame

    sprite = _get_text_surface(**kwargs)
    sprite.mounted = True

    globals.all_sprites.add(sprite)
    globals.map_key_sprite[sprite.key] = sprite
    globals.to_render_keys.add(sprite.key)

    return sprite


def mount_sprite(sprite):
    if sprite.key in globals.to_render_keys:
        # already in to render queue
        return sprite

    print("Rendered", sprite.key)

    globals.all_sprites.add(sprite)
    globals.map_key_sprite[sprite.key] = sprite
    globals.to_render_keys.add(sprite.key)

    return sprite


def unmount_sprite(sprite):
    globals.all_sprites.remove(sprite)
    globals.to_render_keys.discard(sprite.key)

    return sprite


def refill_screen():
    globals.DISPLAYSURF.fill((0, 0, 20))

def reset():
    globals.to_render_keys.clear()
    globals.map_key_sprite.clear()
    globals.all_sprites.empty()


def draw_sprites():
    refill_screen()

    for sprite in globals.all_sprites.sprites():
        if sprite.key not in globals.to_render_keys:
            globals.all_sprites.remove(sprite.key)

    # all_sprites.update()

    globals.all_sprites.draw(globals.DISPLAYSURF)
    pygame.display.flip()
