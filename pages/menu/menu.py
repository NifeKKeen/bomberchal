import globals, sys
from utils import paint_api
from utils.interaction_api import is_clicked
from utils.sound_api import play_menu_music, stop_music
from pages.navigation import navigate


mute_button_sprite = None
play_button_sprite = None
customization_button_sprite = None
settings_button_sprite = None
quit_button_sprite = None


def menu(is_setup=False):
    global mute_button_sprite, play_button_sprite, customization_button_sprite, settings_button_sprite, quit_button_sprite
    if is_setup:
        play_menu_music(volume=.2)

        mute_button_sprite = paint_api.mount_rect(  #region parameters
            px_x=globals.CENTER_X - 350,
            px_y=globals.CENTER_Y - 200,
            px_w=65,
            px_h=65,
            layer=globals.BUTTON_LAYER,
            align="center",
            image_path=globals.MUTED_IMG_PATH1 if globals.music_muted else globals.UNMUTED_IMG_PATH1,

            key="mute",
        )  #endregion

        play_button_sprite = paint_api.mount_rect(  #region parameters
            px_x=globals.CENTER_X,
            px_y=globals.CENTER_Y - 100,
            px_w=500,
            px_h=90,
            layer=globals.BUTTON_LAYER,
            align="center",
            image_path="assets/images/buttons/bar_button.png",

            key="play",
        )  #endregion
        play_pos = play_button_sprite.px_x, play_button_sprite.px_y
        play_button_shadow = paint_api.mount_text(  #region parameters
            px_x=play_pos[0] + globals.SHADOW_OFFSET,
            px_y=play_pos[1] + globals.SHADOW_OFFSET,
            layer=globals.SHADOW_LAYER,
            align="center",
            text="Play",
            font_size=50,
            color=globals.SHADOW_COLOR,

            key="play_text_shadow",
        )  #endregion
        play_button_text = paint_api.mount_text(  #region parameters
            px_x=play_pos[0],
            px_y=play_pos[1],
            layer=globals.TEXT_LAYER,
            align="center",
            text="Play",
            font_size=50,
            color=(255, 255, 255),

            key="play_text",
        )  #endregion

        customization_button_sprite = paint_api.mount_rect(  #region parameters
            px_x=globals.CENTER_X,
            px_y=globals.CENTER_Y,
            px_w=500,
            px_h=90,
            layer=globals.BUTTON_LAYER,
            align="center",
            image_path="assets/images/buttons/bar_button.png",

            key="customization",
        )  #endregion
        customization_pos = customization_button_sprite.px_x, customization_button_sprite.px_y
        customization_button_shadow = paint_api.mount_text(  #region parameters
            px_x=customization_pos[0] + globals.SHADOW_OFFSET,
            px_y=customization_pos[1] + globals.SHADOW_OFFSET,
            layer=globals.SHADOW_LAYER,
            align="center",
            text="Customization",
            font_size=50,
            color=globals.SHADOW_COLOR,

            key="customization_text_shadow",
        )  #endregion
        customization_button_text = paint_api.mount_text(  #region parameters
            px_x=customization_pos[0],
            px_y=customization_pos[1],
            layer=globals.TEXT_LAYER,
            align="center",
            text="Customization",
            font_size=50,
            color=(255, 255, 255),

            key="customization_text",
        )  #endregion

        settings_button_sprite = paint_api.mount_rect(  #region parameters
            px_x=globals.CENTER_X - 128,
            px_y=globals.CENTER_Y + 100,
            px_w=246,
            px_h=90,
            layer=globals.BUTTON_LAYER,
            align="center",
            image_path="assets/images/buttons/bar_button.png",

            key="settings",
        )  #endregion
        settings_pos = settings_button_sprite.px_x, settings_button_sprite.px_y
        settings_button_shadow = paint_api.mount_text(  #region parameters
            px_x=settings_pos[0] + globals.SHADOW_OFFSET,
            px_y=settings_pos[1] + globals.SHADOW_OFFSET,
            layer=globals.SHADOW_LAYER,
            align="center",
            text="Settings",
            font_size=50,
            color=globals.SHADOW_COLOR,

            key="settings_text_shadow",
        )  #endregion
        settings_button_text = paint_api.mount_text(  #region parameters
            px_x=settings_pos[0],
            px_y=settings_pos[1],
            layer=globals.TEXT_LAYER,
            align="center",
            text="Settings",
            font_size=50,
            color=(255, 255, 255),

            key="settings_text",
        )  #endregion

        # scoreboard_button_sprite = paint_api.mount_rect(  #region parameters
        #     px_x=globals.CENTER_X,
        #     px_y=globals.CENTER_Y + 200,
        #     px_w=230,
        #     px_h=90,
        #     layer=globals.BUTTON_LAYER,
        #     align="center",
        #     image_path="assets/images/buttons/bar_button.png",
        #
        #     key="scoreboard",
        # )
        # scoreboard_pos = scoreboard_button_sprite.px_x, scoreboard_button_sprite.px_y
        # scoreboard_button_shadow = paint_api.mount_text(  #region parameters
        #     px_x = scoreboard_pos[0] + globals.SHADOW_OFFSET,
        #     px_y = scoreboard_pos[1] + globals.SHADOW_OFFSET,
        #     layer=globals.SHADOW_LAYER,
        #     align="center",
        #     text="Scoreboard",
        #     font_size=50,
        #     color=globals.SHADOW_COLOR,
        #
        #     key = "scoreboard_text_shadow",
        # )  #endregion
        # scoreboard_button_text = paint_api.mount_text(  #region parameters
        #     px_x = scoreboard_pos[0],
        #     px_y = scoreboard_pos[1],
        #     layer=globals.TEXT_LAYER,
        #     align="center",
        #     text="Scoreboard",
        #     font_size=50,
        #     color=(255, 255, 255),
        #
        #     key="scoreboard_text",
        # )  #endregion

        quit_button_sprite = paint_api.mount_rect(  #region parameters
            px_x=globals.CENTER_X + 128,
            px_y=globals.CENTER_Y + 100,
            px_w=246,
            px_h=90,
            layer=globals.BUTTON_LAYER,
            align="center",
            image_path="assets/images/buttons/bar_button.png",

            key="quit",
        )  #endregion
        quit_pos = quit_button_sprite.px_x, quit_button_sprite.px_y
        quit_button_shadow = paint_api.mount_text(  #region parameters
            px_x=quit_pos[0] + globals.SHADOW_OFFSET,
            px_y=quit_pos[1] + globals.SHADOW_OFFSET,
            layer=globals.SHADOW_LAYER,
            align="center",
            text="Quit",
            font_size=50,
            color=globals.SHADOW_COLOR,

            key="quit_text_shadow",
        )  #endregion
        quit_button_text = paint_api.mount_text(  #region parameters
            px_x=quit_pos[0],
            px_y=quit_pos[1],
            layer=globals.TEXT_LAYER,
            align="center",
            text="Quit",
            font_size=50,
            color=(255, 255, 255),

            key="quit_text",
        )  #endregion

    if is_clicked(play_button_sprite):
        navigate("game")
    elif is_clicked(settings_button_sprite):
        navigate("menu/settings")
    # elif is_clicked(scoreboard_button_sprite):
    #     navigate("menu/scoreboard")
    elif is_clicked(customization_button_sprite):
        navigate("menu/customization")
    elif is_clicked(quit_button_sprite):
        sys.exit()

    elif is_clicked(mute_button_sprite):
        if globals.music_muted:
            globals.music_muted = False
            play_menu_music(volume=.2)
            mute_button_sprite.set_image_path(globals.UNMUTED_IMG_PATH1)
        else:
            globals.music_muted = True
            stop_music()
            mute_button_sprite.set_image_path(globals.MUTED_IMG_PATH1)
