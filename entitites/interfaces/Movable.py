from utils.helpers import get_pos


class Movable:
    def move_px(self, x=0, y=0):
        self.px_x += x
        self.px_y += y
        self.rect.x += x
        self.rect.y += y
        self.x, self.y = get_pos(self.px_x, self.px_y)
        # globals.frame_game_events.append(("move_px", (x, y)))  # TODO

    def set_px(self, x=0, y=0):
        self.px_x = x
        self.px_y = y
        self.rect.x = x
        self.rect.y = y
        self.x, self.y = get_pos(self.px_x, self.px_y)
