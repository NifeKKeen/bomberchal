import globals
from utils import paint_api
from pages.navigation import navigate
from utils.interaction_api import is_clicked


def settings():
    # paint_api.draw_text("Settings", x=300, y=20, font_size=40, color=(255, 255, 255))

    back_button = paint_api.mount_rect(
        px_y=globals.center_y  + (globals.center_y // 2),
        px_w=200,
        px_h=80,
        key="back",
        image_path="assets/images/buttons/back.png",
        align="center"
        
    )

    if is_clicked(back_button):
        navigate("menu")
