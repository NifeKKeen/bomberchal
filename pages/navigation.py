import globals
from utils.paint_api import reset_frame


def navigate(page_name):
    globals.switched_page_this_frame = True
    reset_frame()

    globals.current_page = page_name
    globals.switched_page = True
