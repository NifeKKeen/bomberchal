# Definitions
- To-render queue — set, which stores keys of sprites that should be displayed in the next loop iteration.
- To mount — add sprite to the `all_sprites` global group that will be displayed in the next render.
- Sprite keys — uniquely defined strings that optimizes the app.

# Quick overview of app lifecycle
- In `main.py` we have a single `while True:` loop, which calls functions that will render needed pages, these functions are located only as `/pages/[page_dir]/[page_name].py`.
- For each frame, user events, game state etc. are stored as the global variables, in the corresponding sections in `globals.py`.


# Global variables
- All global variables (unless needed only for one module) should be declared in `globals.py`.
- All global variables must be used like this `globals.[attribute]`.
- All global variables must be updated like this `globals.[attribute] = value`.
- 

# `SurfaceSprite` class
- `SurfaceSprite` inherits `pygame.sprite.Sprite` class. Its on screen positioning based on the `rect` attribute. `px_x`, `px_y`, `px_w`, `px_h` must be synchronized with `rect.x`, `rect.y`, `rect.width`, `rect.height`, respectively.

# Entities
- `Entity` inherits `SurfaceSprite` class, so all entities are actually sprites with additional information and states.
- Be sure that when declaring a new attribute to the class ane its descendant classes, it does not cause any naming conflicts.
- When creating, make sure you are not creating them in game loop repeatedly each tick. They must be created only after a specific event (for example a setup, players's bomb, bonus spawn after a specific period of time).

# Rendering: Usage
- All renders must be called ONLY using functions from `utils/paint_api.py`. Otherwise the render data will not sync.
- To mount a sprite, either create new instance of the SurfaceSprite or use `paint_api.mount_rect`, `paint_api.mount_text`, `paint_api.mount_gif` method.
- If mounted object should not be displayed, it should be removed from to-render queue via `paint_api.unmount(sprite)` or sprite.unmount() method.
- After each render call, it will be mounted until it is unmounted by hand. If you want to mount a sprite only for 1 frame, add argument `dynamic=True` (it is useful in case when you do not want to save additional global variables and unmounting them by hand, but you will tradeoff app performance). 

# Rendering: paint API
- `to_render_keys` stores key values of sprites. It will define which sprite to render in the current frame.
- `map_key_sprite` stones keys and corresponding sprites. It is not synced with `to_render_keys`.
- All mounted objects must be in `all_sprites` global variable. It is the instance created by `pygame.sprite.LayeredUpdates()`.

# Relative sprite layers
- 10: Buttons
- [50, 100): text, icons etc.
- 100: popup accumulated layer
- [10, 30): entities
- - [10, 20): obstacles
- - [20, 30): interactable entities


# Page related things:
- Only `main.py` will run with `while True:` loop. Other pages should only update positions, sizes, contents of pygame objects or mount them.
