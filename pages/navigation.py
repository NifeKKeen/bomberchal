import globals


def navigate(page_name):
    globals.switched_page_this_frame = True

    globals.current_page = page_name
    globals.switched_page = True
