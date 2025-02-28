import pygame
import globals
from utils import paint_api
from pages.navigation import navigate
from utils.interaction_api import is_clicked
import settings  # для вызова change_key

def settings():
    # --- Настройки для Bomb Button первого игрока (player_index = 0)
    offered_keys_p0 = [pygame.K_SPACE, pygame.K_a, pygame.K_m, "custom"]
    try:
        current_index0 = offered_keys_p0.index(globals.controls_players[0]["explosion_key"])
    except ValueError:
        current_index0 = len(offered_keys_p0) - 1

    # Слева — статичный текст
    paint_api.mount_text(
        px_x=globals.center_x - 300,
        px_y=globals.center_y - 120,
        key="label_p0",
        text="Bomb button for player1",
        font_size=20,
        color=(255,255,255)
    )
    # Кнопка-стрелка влево
    left_arrow_p0 = paint_api.mount_rect(
        px_x=globals.center_x - 50,
        px_y=globals.center_y - 120,
        px_w=40,
        px_h=40,
        key="left_arrow_p0",
        # image_path="assets/images/buttons/arrow_left.png",
        align="center"
    )
    # Текущее выбранное значение (отображается как текст)
    current_key_text_p0 = pygame.key.name(offered_keys_p0[current_index0] if offered_keys_p0[current_index0] != "custom" else pygame.K_0)
    display_p0 = paint_api.mount_text(
        px_x=globals.center_x,
        px_y=globals.center_y - 300,
        key="display_p0",
        text=current_key_text_p0,
        font_size=20,
        color=(255,255,0)
    )
    # Кнопка-стрелка вправо
    right_arrow_p0 = paint_api.mount_rect(
        px_x=globals.center_x + 50,
        px_y=globals.center_y - 120,
        px_w=40,
        px_h=40,
        key="right_arrow_p0",
        # image_path="assets/images/buttons/arrow_right.png",
        align="center"
    
    # Обработка кликов для первого игрока
    if is_clicked(left_arrow_p0):
        new_index0 = (current_index0 - 1) % len(offered_keys_p0)
        new_key0 = offered_keys_p0[new_index0]
        if new_key0 == "custom":
            new_key0 = pygame.K_0
        settings.change_key(0, "explosion_key", new_key0)
        print("Player1 bomb key:", globals.controls_players[0]["explosion_key"])
    if is_clicked(right_arrow_p0):
        new_index0 = (current_index0 + 1) % len(offered_keys_p0)
        new_key0 = offered_keys_p0[new_index0]
        if new_key0 == "custom":
            new_key0 = pygame.K_0
        settings.change_key(0, "explosion_key", new_key0)
        print("Player1 bomb key:", globals.controls_players[0]["explosion_key"])

    # --- Настройки для Bomb Button второго игрока (player_index = 1)
    offered_keys_p1 = [pygame.K_RETURN, pygame.K_SPACE, pygame.K_m, "custom"]
    try:
        current_index1 = offered_keys_p1.index(globals.controls_players[1]["explosion_key"])
    except ValueError:
        current_index1 = len(offered_keys_p1) - 1

    # Слева — статичный текст
    paint_api.mount_text(
        px_x=globals.center_x - 300,
        px_y=globals.center_y - 50,
        key="label_p1",
        text="Bomb button for player2",
        font_size=20,
        color=(255,255,255),
    )
    # Кнопка-стрелка влево
    left_arrow_p1 = paint_api.mount_rect(
        px_x=globals.center_x - 50,
        px_y=globals.center_y - 50,
        px_w=40,
        px_h=40,
        key="left_arrow_p1",
        # image_path="assets/images/buttons/arrow_left.png",
        align="center"
    )
    # Текущее выбранное значение (отображается как текст)
    current_key_text_p1 = pygame.key.name(offered_keys_p1[current_index1] if offered_keys_p1[current_index1] != "custom" else pygame.K_0)
    display_p1 = paint_api.mount_text(
        px_x=globals.center_x,
        px_y=globals.center_y - 50,
        key="display_p1",
        text=current_key_text_p1,
        font_size=20,
        color=(255,255,0)
    )
    # Кнопка-стрелка вправо
    right_arrow_p1 = paint_api.mount_rect(
        px_x=globals.center_x + 50,
        px_y=globals.center_y - 50,
        px_w=40,
        px_h=40,
        key="right_arrow_p1",
        # image_path="assets/images/buttons/arrow_right.png",
        align="center"
    )
    # Обработка кликов для второго игрока
    if is_clicked(left_arrow_p1):
        new_index1 = (current_index1 - 1) % len(offered_keys_p1)
        new_key1 = offered_keys_p1[new_index1]
        if new_key1 == "custom":
            new_key1 = pygame.K_0
        settings.change_key(1, "explosion_key", new_key1)
        print("Player2 bomb key:", globals.controls_players[1]["explosion_key"])
    if is_clicked(right_arrow_p1):
        new_index1 = (current_index1 + 1) % len(offered_keys_p1)
        new_key1 = offered_keys_p1[new_index1]
        if new_key1 == "custom":
            new_key1 = pygame.K_0
        settings.change_key(1, "explosion_key", new_key1)
        print("Player2 bomb key:", globals.controls_players[1]["explosion_key"])

    # Кнопка возврата в меню
    back_button = paint_api.mount_rect(
        px_y=globals.center_y + (globals.center_y // 2),
        px_w=200,
        px_h=80,
        key="back",
        image_path="assets/images/buttons/back.png",
        align="center"
    )
    if is_clicked(back_button):
        navigate("menu")
