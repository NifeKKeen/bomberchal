import pygame

import globals

def format_surface_id_to_key(surface_id):
    return "-sid_" + str(surface_id)


class SurfaceSprite(pygame.sprite.Sprite):
    SurfaceId = 0

    def __init__(self, **kwargs):
        super().__init__()

        self.x = kwargs.get("x", 0)  # position x in board (from left) [целые коорды]
        self.y = kwargs.get("y", 0)  # position x in board (from top) [целые коорды]
        self.px_x = kwargs.get("px_x", 0)  # position x in pixels (from left) [пиксельные коорды]
        self.px_y = kwargs.get("px_y", 0)  # position y in pixels (from top) [пиксельные коорды]
        self.px_w = kwargs.get("px_w", 1)  # width in pixels
        self.px_h = kwargs.get("px_h", 1)  # height in pixels

        self.layer = kwargs.get("layer", 0)  # Like z-index in CSS

        self.surface_id = SurfaceSprite.SurfaceId
        self.key = kwargs.get("key", format_surface_id_to_key(self.surface_id))
        SurfaceSprite.SurfaceId += 1

        self.image = pygame.Surface([self.px_w, self.px_h])  # IMPORTANT!
        self.image.set_colorkey((0, 0, 0))  # color to make transparent

        self.image.fill((255, 0, 255))  # if there are no image
        pygame.draw.rect(self.image, (255, 255, 255), pygame.Rect((0, 0, self.px_w, self.px_h)))

        self.rect = self.image.get_rect()
        self.rect.x = self.px_x
        self.rect.y = self.px_y


def _get_surface(**kwargs):
    # if surface_id is not specified, generate a new surface with its unique id
    # otherwise, try to get surface from globals.map_key_sprite with this surface_id

    px_x = kwargs.get("px_x", 0)
    px_y = kwargs.get("px_y", 0)
    px_w = kwargs.get("px_w", 1)
    px_h = kwargs.get("px_h", 1)
    surface_key = kwargs.get("key", None)

    if surface_key is None:
        surface_sprite = SurfaceSprite(px_x=px_x, px_y=px_y, px_w=px_w, px_h=px_h)
    else:
        surface_sprite = globals.map_key_sprite[surface_key]

    return surface_sprite


def set_sprite(sprite):
    if sprite.surface_id in globals.to_render_keys:
        return

    key = sprite.key
    globals.map_key_sprite[key] = sprite
    globals.to_render_keys.add(key)


def draw_rect(**kwargs):
    px_x = kwargs.get("px_x", 0)
    px_y = kwargs.get("px_y", 0)
    px_w = kwargs.get("px_w", 1)
    px_h = kwargs.get("px_h", 1)
    key = kwargs.get("key", None)

    if key in globals.to_render_keys:
        # This sprite already exists in render queue
        return

    sprite = _get_surface(px_x=px_x, px_y=px_y, px_w=px_w, px_h=px_h)

    if key:
        sprite.key = key

    print("Rendered", sprite.key)
    # rect = sprite.image.get_rect()
    pygame.draw.rect(sprite.image, (255, 255, 255), pygame.Rect((0, 0, sprite.px_w, sprite.px_h)))

    globals.all_sprites.add(sprite)
    globals.map_key_sprite[key] = sprite
    globals.to_render_keys.add(key)


def refill_screen():
    globals.DISPLAYSURF.fill((0, 0, 20))


def reset():
    globals.to_render_keys.clear()
    globals.map_key_sprite.clear()
    globals.all_sprites.empty()


def draw_sprites():
    refill_screen()

    will_be_rendered_keys = set()

    for (surface_id, sprite) in globals.map_key_sprite.items():
        if surface_id not in globals.to_render_keys:
            globals.all_sprites.remove(sprite)
            globals.map_key_sprite.pop(sprite.key)

    for sprite in globals.all_sprites.sprites():
        if sprite.key in globals.to_render_keys:
            will_be_rendered_keys.add(sprite.key)

    globals.to_render_keys.clear()
    globals.to_render_keys.update(will_be_rendered_keys)
    # all_sprites.update()

    globals.all_sprites.draw(globals.DISPLAYSURF)
    pygame.display.flip()
