import pygame
from utils import paint_api
from pages.navigation import navigate
from utils.interaction_api import is_clicked

def settings():
    paint_api.refill_screen()
    paint_api.draw_text("Settings", x=300, y=20, font_size=40, color=(255, 255, 255))
    
    back_button = paint_api.mount_rect(
        px_x=300, px_y=300, px_w=200, px_h=80,
        key="back",
        bg_color=(100, 100, 200),
        border_color=(255, 255, 255),
        border_radius=10,
        title="Back"
    )
    
    if is_clicked(back_button):
        navigate("menu")
    
