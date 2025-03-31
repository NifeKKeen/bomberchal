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


# Bot Types Overview
## 1. Original bot
- Its behaviour is similar to bot in the initial game, Bomberman.
- Doesn't use any pathfinding or advanced logic. Instead, it moves in straight line based on its current direction. If it encounters obstacle or bot, it reverses direction (UP ↔ DOWN, LEFT ↔ RIGHT).
- Occasionally (1% chance every tick), it may randomly flip direction to simulate randomness and less predictability.
- Rarely (0.01% chance every tick), it will place a bomb at random intervals, regardless of surroundings.
- This type of bot is mainly useful for acting like background "filler" enemies. It neither pursues players nor tries to avoid danger.

## 2. Wandering bot
- Designed to avoid danger. Its logic uses Dijkstra algorithm to calculate the safest possible tiles based on weights assigned from nearby bombs, fires, players.
- Among all safest possible tiles on map, it tries to move toward the farthest one.
- The only type of bot that never spawns bombs. Also, it doesn’t care about bonuses.
- This makes it unpredictable and passive. It survives, not fights.

## 3. Aggressive bot
- Basic attack-oriented bot. Similarly to wandering bot, uses Dijkstra algorithm, but to find the shortest safe path to the nearest player.
- If player is unreachable, switches to the closest safe bonus.
- If there are no bonuses, just goes to farthest safe cell.
- If it's impossible to reach target, but it can spawn bomb and not die (`max_dist > bomb_power`), it does that.
- Considers weights of dangers (bombs, fires) so as not to walk straight into the fire.

## 4. Boss bot
- Repeats behaviour of aggressive bot
- Considered to have improved characteristics: increased `lives`, `bomb_power`, `speed` etc.


## Description of pathfinding and `moving` parameter for bots 2-4
- The main idea is to calculate safety of path using globals.field_weight for 3-4 or self.weight for wandering (weight of every cell):
- - For every obstacle or bot, weight is infinity
- - For every bomb, the closer cell to center of bomb, the greater its weight (`bomb_power + 1` at bomb itself, for adjacent `bomb_power`, and so on)
- - For every fire, weight increases by `10`
- - For every player, weight increases by `its bomb_power + 5`
- In Dijkstra algorithm where we start from `(self.x, self.y)`, we try to minimize max(weighted_dist), if they're equal, minimize sum of dist (just unweighted distances).
- After this algorithm, we can obtain safety of path and unweighted distance to every cell
- In wandering bot's `think()`, if there's cell where bot won't die because of bomb, it will calculate distance to farthest cell. Then set `(dest_x, dest_y)` to one of cells distance to which is `>= max_dist - 5` (not just `== max_dist`, because in practice it turned out that it can choose potentially disadvantageous routes that can go across entire field).
- After saving `(dest_x, dest_y)`, Dijkstra algorithm is run again from this (destination) position. Purpose of these calculations is obtaining `self.prev` array.
- `prev[x][y]` contains the cell from which the transition to `(x, y)` was made. Since we started the second pass from the end point, then `self.prev[self.x][self.y]` will be equal to next will be equal to the next point we go to.


- All of the above happens only when `self.moving = 0`. This means in current tick bot is calculating all stuff, but not moving.
- At the end of `self.moving = 0` block, this parameter becomes equal to `1`. That means the bot starts moving.
- According to the array `self.prev`, it can easily get next cell and direction to it.
- If there is no next cell (bot is already in its target cell) or somehow `self.prev[x][y] = (-1, -1)`, then it goes into computation (`self.moving = 0` block) again


- Also, since coordinates in field are determined by the center of bot, if it needs to turn, but there is an obstacle in previous cell, then he won't be able to go any further.
- `.#`
- `**`
- To make it more clear, if it's like above (`#` is obstacle, `*` is bot moving left) and bot's field coordinates are being changed from right to left, then his right side will not be able to pass because of the obstacle above him => stuck.
- To prevent this, `self.moving = 2` is implemented. Its goal is to make bot fit entirely within one cell. Of course, its speed and direction are taken into account.
- If the bot position is aligned, we return the previous value to `moving`