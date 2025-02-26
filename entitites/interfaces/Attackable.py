class Attackable:
    def move_px(self, x=0, y=0):
        self.px_x += x
        self.px_y += y
        self.rect.x += x
        self.rect.y += y
        globals.frame_game_events.append(("move_px", (x, y)))

    def set_px(self, x=0, y=0):
        self.px_x = x
        self.px_y = y
        self.rect.x = x
        self.rect.y = y

