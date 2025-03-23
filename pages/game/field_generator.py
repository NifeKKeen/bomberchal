import globals
import random

# Generator like in real game
def generate(cols, rows, game_mode):
    boss_fight = (True if game_mode == "bossfight" else False)
    field = [
        [globals.U_OBSTACLE_CELL if (not boss_fight and (i % 2 == 0 and j % 2 == 0) or
                                    i == 0 or i == cols - 1 or j == 0 or j == rows - 1) else globals.VOID_CELL
                                    for j in range(rows)] for i in range(cols)
    ]
    bot_count = [3, 3, 3, 0] # original, wandering, aggressive, boss
    if boss_fight:
        bot_count = [0] * 4 # only boss, and position will be defined later

    obstacle_count = 50
    objects = []
    current = 0
    max_bomb_power = 8

    for x in range(1, cols - 1):
        for y in range(1, rows - 1):
            if field[x][y] == globals.U_OBSTACLE_CELL:
                continue
            if x - 1 + y - 1 <= max_bomb_power + 1: # Ability for player 1 to leave and not insta-die
                continue
            elif cols - 2 - x + rows - 2 - y <= max_bomb_power + 1: # Same for player 2
                continue
            objects.append(current)
            current += 1

    random.shuffle(objects)
    current = 0

    for x in range(1, cols - 1):
        for y in range(1, rows - 1):
            if boss_fight and x == cols // 2 and y == rows // 2:
                field[x][y] = globals.BOSS_BOT_CELL
                continue

            if field[x][y] == globals.U_OBSTACLE_CELL:
                continue
            if x - 1 + y - 1 <= max_bomb_power + 1:
                field[x][y] = globals.VOID_CELL
                continue
            elif cols - 2 - x + rows - 2 - y <= max_bomb_power + 1:
                field[x][y] = globals.VOID_CELL
                continue

            elif objects[current] < obstacle_count:
                field[x][y] = globals.D_OBSTACLE_CELL
            elif objects[current] < obstacle_count + bot_count[0]:
                field[x][y] = globals.ORIGINAL_BOT_CELL
            elif objects[current] < obstacle_count + sum(bot_count[:2]):
                field[x][y] = globals.WANDERING_BOT_CELL
            elif objects[current] < obstacle_count + sum(bot_count[:3]):
                field[x][y] = globals.AGGRESSIVE_BOT_CELL
            elif objects[current] < obstacle_count + sum(bot_count[:4]):
                field[x][y] = globals.BOSS_BOT_CELL
            else:
                field[x][y] = globals.VOID_CELL
            current += 1
    return field


# Maze generator, probably will be used for smth
def generate_maze(cols, rows):
    field = [
        [globals.U_OBSTACLE_CELL for j in range(rows)] for i in range(cols)
    ]
    field[1][1] = globals.VOID_CELL

    max_depth = 3
    directions = globals.BFS_DIRECTIONS

    def dfs(x, y):
        if random.randint(1, 50) <= 30: #for more straight passes
            random.shuffle(directions)

        for dx, dy in directions:
            nx, ny = x + 2 * dx, y + 2 * dy
            if nx < 1 or nx >= globals.cols - 1 or ny < 1 or ny >= globals.rows - 1:
                continue
            if field[nx][ny] == globals.VOID_CELL:
                continue
            field[nx][ny] = globals.VOID_CELL
            field[x + dx][y + dy] = globals.VOID_CELL
            dfs(nx, ny)

    dfs(1, 1)
    for i in field:
        print(i)
    return field
