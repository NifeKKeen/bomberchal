import globals, pygame, configparser, os
from utils import paint_api
from utils.interaction_api import is_clicked, get_last_pressed_key
from utils.sound_api import play_menu_music
from pages.navigation import navigate


CONFIG_FILE = "pages/menu/config.ini"


def load_config():
    if not os.path.exists(CONFIG_FILE):
        globals.game_mode = "default"
        return
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    if "Controls" in config:
        key1_str = config.get("Controls", "explosion_key_p1", fallback="space").strip()
        key2_str = config.get("Controls", "explosion_key_p2", fallback="m").strip()

        globals.controls_players[0]["explosion_key"] = parse_key(key1_str)
        globals.controls_players[1]["explosion_key"] = parse_key(key2_str)
    if "Game" in config:
        globals.game_mode = config.get("Game", "mode", fallback="default")  # исправлено: читаем ключ "mode"
    else:
        globals.game_mode = "default"


def parse_key(key_str):
    if key_str.lower() == "custom":
        return "custom"
    try:
        return int(key_str)  
    except ValueError:
        return pygame.key.key_code(key_str.lower())  


def save_config():
    config = configparser.ConfigParser()
    config["Controls"] = {
        "explosion_key_p1": str(globals.controls_players[0]["explosion_key"]),
        "explosion_key_p2": str(globals.controls_players[1]["explosion_key"])
    }
    config["Game"] = {"mode": str(globals.game_mode)}
    with open(CONFIG_FILE, "w") as configfile:
        config.write(configfile)


def update_display(text_sprite, player_index, waiting):
    key_val = globals.controls_players[player_index]["explosion_key"]
    display_text = "Press key..." if waiting else (pygame.key.name(key_val) if key_val != "custom" else "Custom")
    text_sprite.set_text(display_text)


left_arrow_p0 = None
display_p0 = None
right_arrow_p0 = None
left_arrow_p1 = None
display_p1 = None
right_arrow_p1 = None
default_button = None
default_button_text = None
boss_button = None
boss_button_text = None
back_button = None
back_button_text = None
bomb_mute_button_sprite = None

current_key_text_p0 = None
current_key_text_p1 = None

def mount_sprites():
    global left_arrow_p0, display_p0, right_arrow_p0
    global left_arrow_p1, display_p1, right_arrow_p1
    global default_button, default_button_text
    global boss_button, boss_button_text
    global back_button, back_button_text
    global current_key_text_p0, current_key_text_p1
    global bomb_mute_button_sprite
    paint_api.mount_text(  #region parameters
        px_x=globals.CENTER_X,
        px_y=globals.CENTER_Y - 250,
        layer=globals.TEXT_LAYER,
        align="center",
        text="Change bomb button",
        font_size=40,
        color=(255, 255, 255),

        key="change_bomb_button",
    )  #endregion
    paint_api.mount_text(  #region parameters
        px_x=globals.CENTER_X - 350,
        px_y=globals.CENTER_Y - 170,
        layer=globals.TEXT_LAYER,
        text="for player1",
        font_size=30,
        color=(255, 255, 255),

        key="label_p0",
    )  #endregion

    left_arrow_p0 = paint_api.mount_rect(  #region parameters
        px_x=globals.CENTER_X - 150,
        px_y=globals.CENTER_Y - 185,
        px_w=75,
        px_h=75,
        layer=globals.BUTTON_LAYER,
        image_path="assets/images/buttons/left.png",

        key="left_arrow_p0",
    )  #endregion
    display_p0 = paint_api.mount_text(  #region parameters
        px_x=globals.CENTER_X + 35,
        px_y=globals.CENTER_Y - 150,
        layer=globals.TEXT_LAYER,
        align="center",
        text=current_key_text_p0,
        font_size=25,
        color=(255, 255, 0),

        key="display_p0",
    )  #endregion
    right_arrow_p0 = paint_api.mount_rect(  #region parameters
        px_x=globals.CENTER_X + 150,
        px_y=globals.CENTER_Y - 185,
        px_w=75,
        px_h=75,
        layer=globals.BUTTON_LAYER,
        image_path="assets/images/buttons/right.png",

        key="right_arrow_p0",
    )  #endregion

    paint_api.mount_text(  #region parameters
        px_x=globals.CENTER_X - 350,
        px_y=globals.CENTER_Y - 50,
        layer=globals.TEXT_LAYER,
        text="for player2",
        font_size=30,
        color=(255, 255, 255),

        key="label_p1",
    )  #endregion

    left_arrow_p1 = paint_api.mount_rect(  #region parameters
        px_x=globals.CENTER_X - 150,
        px_y=globals.CENTER_Y - 65,
        px_w=75,
        px_h=75,
        layer=globals.BUTTON_LAYER,
        image_path="assets/images/buttons/left.png",

        key="left_arrow_p1",
    )  #endregion
    display_p1 = paint_api.mount_text(  #region parameters
        px_x=globals.CENTER_X + 35,
        px_y=globals.CENTER_Y - 35,
        layer=globals.TEXT_LAYER,
        align="center",
        text=current_key_text_p1,
        font_size=25,
        color=(255, 255, 0),

        key="display_p1",
    )  #endregion
    right_arrow_p1 = paint_api.mount_rect(  #region parameters
        px_x=globals.CENTER_X + 150,
        px_y=globals.CENTER_Y - 65,
        px_w=75,
        px_h=75,
        layer=globals.BUTTON_LAYER,
        image_path="assets/images/buttons/right.png",

        key="right_arrow_p1",
    )  #endregion

    paint_api.mount_text(  #region parameters
        px_x=globals.CENTER_X - 350,
        px_y=globals.CENTER_Y + 50,
        layer=globals.TEXT_LAYER,
        text="Game mode",
        font_size=30,
        color=(255, 255, 255),

        key="game_mode",
    )  #endregion

    default_button = paint_api.mount_rect(  #region parameters
        px_x=globals.CENTER_X - 65,
        px_y=globals.CENTER_Y + 70,
        px_w=170,
        px_h=60,
        layer=globals.BUTTON_LAYER,
        align="center",
        image_path="assets/images/buttons/bar_button.png",

        key="default",
    )  #endregion
    default_pos = default_button.px_x, default_button.px_y
    default_button_shadow = paint_api.mount_text(  #region parameters
        px_x=default_pos[0] + globals.SHADOW_OFFSET,
        px_y=default_pos[1] + globals.SHADOW_OFFSET,
        layer=globals.SHADOW_LAYER,
        align="center",
        text="Default",
        font_size=40,
        color=globals.SHADOW_COLOR,

        key="default_text_shadow",
    )  #endregion
    default_button_text = paint_api.mount_text(  #region parameters
        px_x=default_pos[0],
        px_y=default_pos[1],
        layer=globals.TEXT_LAYER,
        align="center",
        text="Default",
        font_size=40,
        color=(255, 255, 255),

        key="default_text",
    )  #endregion

    boss_button = paint_api.mount_rect(  #region parameters
        px_x=globals.CENTER_X + 150,
        px_y=globals.CENTER_Y + 70,
        px_w=250,
        px_h=60,
        layer=globals.BUTTON_LAYER,
        align="center",
        image_path="assets/images/buttons/bar_button.png",

        key="boss",
    )  #endregion
    boss_pos = boss_button.px_x, boss_button.px_y
    boss_button_shadow = paint_api.mount_text(  #region parameters
        px_x=boss_pos[0] + globals.SHADOW_OFFSET,
        px_y=boss_pos[1] + globals.SHADOW_OFFSET,
        layer=globals.SHADOW_LAYER,
        align="center",
        text="Boss Fight",
        font_size=40,
        color=globals.SHADOW_COLOR,

        key="boss_text_shadow",
    )  #endregion
    boss_button_text = paint_api.mount_text(  #region parameters
        px_x=boss_pos[0],
        px_y=boss_pos[1],
        layer=globals.TEXT_LAYER,
        align="center",
        text="Boss Fight",
        font_size=40,
        color=(255, 255, 255),

        key="boss_text",
    )  #endregion

    paint_api.mount_text(
        px_x=globals.CENTER_X - 350,
        px_y=globals.CENTER_Y + 150,
        layer=globals.TEXT_LAYER,
        text="Mute bomb sound",
        font_size=30,
        color=(255, 255, 255),

        key="bomb_mute_text",
    )
    bomb_mute_button_sprite = paint_api.mount_rect(  #region parameters
            px_x=globals.CENTER_X + 20,
            px_y=globals.CENTER_Y + 165,
            px_w=65,
            px_h=65,
            layer=globals.BUTTON_LAYER,
            align="center",
            image_path=globals.MUTED_IMG_PATH2 if globals.sound_muted else globals.UNMUTED_IMG_PATH2,

            key="bomb_mute",
    )  #endregion
    back_button = paint_api.mount_rect(  #region parameters
        px_x=globals.CENTER_X,
        px_y=globals.CENTER_Y + 300,
        px_w=350,
        px_h=80,
        layer=globals.BUTTON_LAYER,
        align="center",
        image_path="assets/images/buttons/bar_button.png",

        key="back",
    )  #endregion
    back_pos = back_button.px_x, back_button.px_y
    back_button_shadow = paint_api.mount_text(  #region parameters
        px_x=back_pos[0] + globals.SHADOW_OFFSET,
        px_y=back_pos[1] + globals.SHADOW_OFFSET,
        layer=globals.SHADOW_LAYER,
        align="center",
        text="Back",
        font_size=50,
        color=globals.SHADOW_COLOR,

        key="back_text_shadow",
    )  #endregion
    back_button_text = paint_api.mount_text(  #region parameters
        px_x=back_pos[0],
        px_y=back_pos[1],
        layer=globals.TEXT_LAYER,
        align="center",
        text="Back",
        font_size=50,
        color=(255, 255, 255),

        key="back_text",
    )  #endregion


def settings(is_setup=False):
    global left_arrow_p0, display_p0, right_arrow_p0
    global left_arrow_p1, display_p1, right_arrow_p1
    global default_button, default_button_text
    global boss_button, boss_button_text
    global back_button, back_button_text
    global current_key_text_p0, current_key_text_p1

    load_config()
    offered_keys_p0 = [pygame.K_SPACE, pygame.K_v, pygame.K_x, "custom"]
    try:
        current_index0 = offered_keys_p0.index(globals.controls_players[0]["explosion_key"])
    except ValueError:
        current_index0 = len(offered_keys_p0) - 1

    waiting_for_key1 = globals.controls_players[0]["explosion_key"] == "custom"

    current_key_text_p0 = "Custom" if offered_keys_p0[current_index0] == "custom" else pygame.key.name(offered_keys_p0[current_index0])

    offered_keys_p1 = [pygame.K_RETURN, pygame.K_m, pygame.K_n, "custom"]
    try:
        current_index1 = offered_keys_p1.index(globals.controls_players[1]["explosion_key"])
    except ValueError:
        current_index1 = len(offered_keys_p1) - 1

    waiting_for_key2 = globals.controls_players[1]["explosion_key"] == "custom"

    current_key_text_p1 = "Custom" if offered_keys_p1[current_index1] == "custom" else pygame.key.name(offered_keys_p1[current_index1])

    if is_setup:
        play_menu_music(volume=.2)
        mount_sprites()

    if is_clicked(left_arrow_p0) or is_clicked(right_arrow_p0):
        new_index0 = (current_index0 + (-1 if is_clicked(left_arrow_p0) else 1)) % len(offered_keys_p0)
        new_key0 = offered_keys_p0[new_index0]
        if new_key0 != "custom" and new_key0 == globals.controls_players[1]["explosion_key"]:
            display_p0.set_text("Duplicate!")
        else:
            if new_key0 == "custom":
                globals.controls_players[0]["explosion_key"] = "custom"
                waiting_for_key1 = True
            else:
                globals.controls_players[0]["explosion_key"] = new_key0
                waiting_for_key1 = False
            update_display(display_p0, 0, waiting_for_key1)
            save_config()
    if waiting_for_key1:
        pressed_key = get_last_pressed_key()
        if pressed_key is not None:
            if pressed_key == globals.controls_players[1]["explosion_key"]:
                display_p0.set_text("Duplicate!")
            else:
                globals.controls_players[0]["explosion_key"] = pressed_key
                waiting_for_key1 = False
                update_display(display_p0, 0, waiting_for_key1)
                save_config()

    if is_clicked(left_arrow_p1) or is_clicked(right_arrow_p1):
        new_index1 = (current_index1 + (-1 if is_clicked(left_arrow_p1) else 1)) % len(offered_keys_p1)
        new_key1 = offered_keys_p1[new_index1]
        if new_key1 != "custom" and new_key1 == globals.controls_players[0]["explosion_key"]:
            display_p1.set_text("Duplicate!")
        else:
            if new_key1 == "custom":
                globals.controls_players[1]["explosion_key"] = "custom"
                waiting_for_key2 = True
            else:
                globals.controls_players[1]["explosion_key"] = new_key1
                waiting_for_key2 = False
            update_display(display_p1, 1, waiting_for_key2)
            save_config()
    if waiting_for_key2:
        pressed_key = get_last_pressed_key()
        if pressed_key is not None:
            if pressed_key == globals.controls_players[0]["explosion_key"]:
                display_p1.set_text("Duplicate!")
            else:
                globals.controls_players[1]["explosion_key"] = pressed_key
                waiting_for_key2 = False
                update_display(display_p1, 1, waiting_for_key2)
                save_config()




    if is_clicked(default_button):
        globals.game_mode = "default"
        print("default clicked")
        save_config()
    if is_clicked(boss_button):
        print("boss clicked")
        globals.game_mode = "bossfight"
        save_config()

    if globals.game_mode == "default":
        print("default")
        default_button_text.set_color((255, 255, 0))
        boss_button_text.set_color((255, 255, 255))
    elif (globals.game_mode == "bossfight"):
        print()
        boss_button_text.set_color((255, 255, 0))
        default_button_text.set_color((255, 255, 255))

    if is_clicked(bomb_mute_button_sprite):
        if globals.sound_muted:
            globals.sound_muted = False
            bomb_mute_button_sprite.set_image_path(globals.UNMUTED_IMG_PATH2)
        else:
            globals.sound_muted = True
            bomb_mute_button_sprite.set_image_path(globals.MUTED_IMG_PATH2)
    if is_clicked(back_button):
        if globals.controls_players[0]["explosion_key"] == "custom":
            globals.controls_players[0]["explosion_key"] = pygame.K_SPACE
        if globals.controls_players[1]["explosion_key"] == "custom":
            globals.controls_players[1]["explosion_key"] = pygame.K_RETURN
        save_config()
        navigate("menu")
