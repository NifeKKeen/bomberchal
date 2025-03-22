# Definitions
- To-render queue — set, which stores keys of sprites that should be displayed in the next loop iteration.
- To mount — add sprite to the `all_sprites` global group that will be displayed in the next render.
- Sprite keys — uniquely defined strings that optimizes the app.

# Quick overview of app lifecycle
- In `main.py` we have the single `while True:` loop, which calls functions that will render page, these functions are located only in `/pages/[module_name].py` directory.
- Event types of events fires from user are collected in `global.frame_events` set, which other modules can access efficiently. `global.frame_events` will be updated and reset each frame.


# Global variables
- All global variables should be declared in `globals.py`
- All global variables must be used like this `globals.[attribute]`
- All global variables must be updated like this `globals.[attribute] = value`

# `SurfaceSprite` class
- `SurfaceSprite` inherits `pygame.sprite.Sprite` class. Its positioning based on `rect` attribute.

# Entities
- `Entity` inherits `SurfaceSprite` class, so all entities are actually sprites with additional information.
- Be sure that when declaring a new attribute, it does not cause any naming conflicts.
- For each entity, when creating, define a unique key so that it will not cause excessive renders each frame.

# Rendering: Usage
- All renders must be called ONLY using functions from `utils/paint_api.py`. Otherwise the render data will not sync.
- To mount a sprite, use `paint_api.mount_sprite` method.
- If mounted object should not be displayed, it should be removed from to-render queue via `paint_api.unmount(sprite)` method.

# Rendering: paint API
- `to_render_keys` and `map_key_sprite` variables are closely related. They must be synced.
- All mounted objects must be in `all_sprites` global variable. It is the instance created by `pygame.sprite.LayeredUpdates()`.

# Relative sprite layers
- 10: Buttons
- [50, 100): text, icons etc.
- 100: popup accumulated layer
- [10, 30): entities
- - [10, 20): obstacles
- - [20, 30): interactable entities


# Page related things:
- Only `main.py` will run with `while True:` loop. Other pages should only update positions of pygame objects or mount them.
