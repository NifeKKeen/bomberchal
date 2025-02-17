import globals

# from pages.settings import  settings

def navigate(page_name):
    if page_name == "game":
        globals.switched_page_this_frame = True
        globals.current_page = page_name
        globals.switched_page = True
        

    # globals.current_page = page_name
    # globals.switched_page = True
    # if page_name == "settings":
        # settings()