import os
import json
import pygame
import globals
from utils.paint_api import SurfaceSprite  

SCOREBOARD_FILE = "utils/scoreboard.json"

def load_scoreboard_data():
    if not os.path.exists(SCOREBOARD_FILE):
        data = {"scoreboard": []}
        with open(SCOREBOARD_FILE, 'w') as f:
            json.dump(data, f, indent=4)
        return data
    else:
        with open(SCOREBOARD_FILE, 'r') as f:
            try:
                data = json.load(f)
            except Exception:
                data = {"scoreboard": []}
        if "scoreboard" not in data:
            data["scoreboard"] = []
        return data

def save_scoreboard_data(data):
    with open(SCOREBOARD_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def get_scoreboard(mode):
    mode = mode.lower()
    data = load_scoreboard_data()
    scoreboard_list = data.get("scoreboard", [])
    
    if mode in ("pve", "bossfight"):
        key = "pve" if mode == "pve" else "bossfight"
        sorted_list = sorted(
            scoreboard_list,
            key=lambda x: x.get(key, {}).get("score", 0),
            reverse=True
        )
    elif mode == "duel":
        sorted_list = sorted(
            scoreboard_list,
            key=lambda x: (x.get("duel", {}).get("wins", 0),
                           -x.get("duel", {}).get("losses", 0)),
            reverse=True
        )
    else:
        sorted_list = scoreboard_list
    return sorted_list[:5]

def update_score(mode, username, score):
    mode = mode.lower()
    if mode not in ("pve", "bossfight"):
        raise ValueError("update only for pve or bossfight modes.")
    
    key = "pve" if mode == "pve" else "bossfight"
    data = load_scoreboard_data()
    updated = False
    for entry in data["scoreboard"]:
        if entry.get("username") == username:
            if key not in entry:
                entry[key] = {"score": 0}
            if score > entry[key].get("score", 0):
                entry[key]["score"] = score
            updated = True
            break
    if not updated:
        new_entry = {
            "username": username,
            "pve": {"score": score} if mode == "pve" else {"score": 0},
            "bossfight": {"score": score} if mode == "bossfight" else {"score": 0},
            "duel": {"wins": 0, "losses": 0, "draws": 0}
        }
        data["scoreboard"].append(new_entry)
    save_scoreboard_data(data)
    return get_scoreboard(mode)

def update_duel(username, wins=0, losses=0, draws=0):
    data = load_scoreboard_data()
    found = False
    for entry in data["scoreboard"]:
        if entry.get("username") == username:
            duel_data = entry.get("duel", {"wins": 0, "losses": 0, "draws": 0})
            duel_data["wins"] += wins
            duel_data["losses"] += losses
            duel_data["draws"] += draws
            entry["duel"] = duel_data
            found = True
            break
    if not found:
        new_entry = {
            "username": username,
            "pve": {"score": 0},
            "bossfight": {"score": 0},
            "duel": {"wins": wins, "losses": losses, "draws": draws}
        }
        data["scoreboard"].append(new_entry)
    save_scoreboard_data(data)
    return get_scoreboard("duel")

class ScoreboardSprite(SurfaceSprite):
    def __init__(self, mode, **kwargs):
        self.mode = mode.lower()
        self.width = kwargs.get("px_w", 650)
        self.height = kwargs.get("px_h", 400)
        self.font_size = kwargs.get("font_size", 30)
        self.bg_color = kwargs.get("bg_color", (50, 50, 50, 180))
        self.text_color = kwargs.get("text_color", (255, 255, 255))
        self.font_family = kwargs.get("font_family", globals.TEXT_FONT)
        self.key = kwargs.get("key", f"scoreboard_{self.mode}")
        
        kwargs["px_w"] = self.width
        kwargs["px_h"] = self.height
        super().__init__(**kwargs, should_refresh=False)
        self.font = pygame.font.Font(self.font_family, self.font_size)
        self.refresh()

    def refresh(self):
        if self.mode in ("pve", "bossfight"):
            entries = get_scoreboard(self.mode)
        elif self.mode == "duel":
            entries = get_scoreboard("duel")
        else:
            entries = []
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.image.fill(self.bg_color)
        padding = int(self.font_size * 0.8)
        y_offset = 10  
        if self.mode == "duel":
            header_text = f"{'Username':<10} {'Wins':>4} {'Loses':>6} {'Draws':>7}"
            header_surf = self.font.render(header_text, True, self.text_color)
            self.image.blit(header_surf, (10, y_offset))
            y_offset += self.font_size + padding
        else:
            header_text = f"{'Username':<10} {'Score':>6}"
            header_surf = self.font.render(header_text, True, self.text_color)
            self.image.blit(header_surf, (10, y_offset))
            y_offset += self.font_size + padding
        for entry in entries:
            if self.mode in ("pve", "bossfight"):
                key = "pve" if self.mode == "pve" else "bossfight"
                line_text = f"{entry.get('username')}: {entry.get(key, {}).get('score', 0):>13}"
            elif self.mode == "duel":
                duel = entry.get("duel", {"wins": 0, "losses": 0, "draws": 0})
                line_text = f"{entry.get('username', ''):<10} {duel.get('wins', 0):>5} {duel.get('losses', 0):>7} {duel.get('draws', 0):>8}"
            line_surf = self.font.render(line_text, True, self.text_color)
            self.image.blit(line_surf, (10, y_offset))
            y_offset += self.font_size + padding
            if y_offset > self.height - self.font_size:
                break
        self.rect = self.image.get_rect()
        self.rect.x = self.px_x
        self.rect.y = self.px_y
        if self.align == "center":
            self.rect.x -= self.rect.width // 2
            self.rect.y -= self.rect.height // 2
        self.should_refresh = False

def mount_scoreboard(mode, **kwargs):
    for key in list(globals.map_key_sprite.keys()):
        if key.startswith("scoreboard"):
            unmount_scoreboard(globals.map_key_sprite[key])
    sprite = ScoreboardSprite(mode, **kwargs)
    globals.all_sprites.add(sprite)
    globals.map_key_sprite[sprite.key] = sprite
    globals.to_render_keys.add(sprite.key)
    sprite.mounted = True
    return sprite

def unmount_scoreboard(sprite):
    if sprite.key in globals.map_key_sprite:
        globals.all_sprites.remove(sprite)
        globals.to_render_keys.discard(sprite.key)
        sprite.mounted = False
    return sprite
