import globals
import random

# Generator like in real game
def generate(cols, rows):
    field = [
        [globals.U_OBSTACLE_CELL if (i % 2 == 0 and j % 2 == 0) or
                                    i == 0 or i == cols - 1 or j == 0 or j == rows - 1 else globals.VOID_CELL
                                    for j in range(rows)] for i in range(cols)
    ]
    bot_count = 10
    obstacle_count = 2555
    objects = []
    current = 0
    for x in range(1, cols - 1):
        for y in range(1, rows - 1):
            if field[x][y] == globals.U_OBSTACLE_CELL:
                continue
            objects.append(current)
            current += 1

    random.shuffle(objects)
    current = 0
    max_bomb_power = 7

    for x in range(1, cols - 1):
        for y in range(1, rows - 1):
            if field[x][y] == globals.U_OBSTACLE_CELL:
                continue
            if x - 1 + y - 1 <= max_bomb_power + 1: # Ability for player 1 to leave and not insta-die
                field[x][y] = globals.VOID_CELL
                continue
            elif cols - 2 - x + rows - 2 - y <= max_bomb_power + 1: # Same for player 2
                field[x][y] = globals.VOID_CELL
                continue
            elif objects[current] < obstacle_count:
                field[x][y] = globals.D_OBSTACLE_CELL
            elif objects[current] < obstacle_count + bot_count:
                field[x][y] = globals.BOT_CELL
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
    directions = globals.directions

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