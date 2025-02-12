import globals


def navigate(page_name):
    globals.current_page = page_name
    globals.switched_page = True
