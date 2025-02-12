# Global variables
- All global variables should be declared in `globals.py`
- All global variables must be used like this `globals.[attribute]`
- All global variables must be updated like this `globals.[attribute] = [value]`

# Rendering
- All to-render/to-draw objects must be in `all_sprites` global variable. It is the instance created by `pygame.sprite.LayeredUpdates()`.
- If to-render/to-draw object should not be displayed, it should be removed from `all_sprites` manually via `all_sprites.remove()` method.

# Sprite layers
- [0, 100) menu
- [100, 200) game board
- [200, 300) game interactable objects:
- - [200, 250) obstacles
- - [250, 300) entities
- [300, ..) overlay (pause menu)


# Page related things:
- Only `main.py` will run with `while True:` loop. Other pages should only update positions of pygame objects.
