# Global variables
- All global variables should be declared in `main.py`

# Rendering
- All to-render/to-draw objects must be in `all_sprites` global variable. It is the instance created by `pygame.sprite.Group()`.
- If to-render/to-draw object should not be displayed, it should be removed from `all_sprites` manually via `all_sprites.remove()` method.

# Page related things:
- Only `main.py` will run with `while True:` loop. Other pages should only update positions of pygame to-render/to-draw objects.
