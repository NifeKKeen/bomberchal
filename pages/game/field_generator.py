import pygame
from pygame.locals import *

import globals
from utils import helpers
import random
from utils.event_api import is_fired
from utils.paint_api import is_mounted

# Generator like in real game
def generate(rows, cols):
    field = [
        [globals.U_OBSTACLE_CELL if (i % 2 == 0 and j % 2 == 0) or
                                    i == 0 or i == rows - 1 or j == 0 or j == cols - 1 else globals.VOID_CELL
                                    for j in range(cols)] for i in range(rows)
    ]
    for x in range(1, rows - 1):
        for y in range(1, cols - 1):
            if field[x][y] == globals.U_OBSTACLE_CELL:
                continue
            field[x][y] = (globals.D_OBSTACLE_CELL if random.randint(1, 100) <= 10 else globals.VOID_CELL)

    return field

# Maze generator, probably will be used for smth
def generate_maze(rows, cols):
    field = [
        [globals.U_OBSTACLE_CELL for j in range(cols)] for i in range(rows)
    ]
    field[1][1] = globals.VOID_CELL

    max_depth = 3
    directions = globals.directions

    def dfs(x, y):
        if random.randint(1, 50) <= 30: #for more straight passes
            random.shuffle(directions)

        for dx, dy in directions:
            nx, ny = x + 2 * dx, y + 2 * dy
            if nx < 1 or nx >= globals.rows - 1 or ny < 1 or ny >= globals.cols - 1:
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