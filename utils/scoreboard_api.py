import os
import json
import globals

SCOREBOARD_FILE = 'scoreboard.json'

def load_scoreboard():
    if os.path.exists(SCOREBOARD_FILE):
        with open(SCOREBOARD_FILE, 'r') as f:
            return json.load(f)
    return {"pve": {}, "bossfight": {}, "duel": {}}

def save_scoreboard(scoreboard):
    with open(SCOREBOARD_FILE, 'w') as f:
        json.dump(scoreboard, f, indent=4)

def add_payload(user_name, game_type, payload):
    scoreboard = load_scoreboard()  
    if game_type not in scoreboard:
        scoreboard[game_type] = {} if game_type in ("pve", "bossfight") else {}

    if game_type in ("pve", "bossfight"):
        if payload.get("user_name") != user_name:
            raise ValueError("Имя пользователя в payload не соответствует.")
        value = payload.get("value", 0)
        scoreboard[game_type].setdefault(user_name, 0)
        scoreboard[game_type][user_name] += value
    elif game_type == "duel":
        for entry in payload:
            uname = entry.get("user_name1") or entry.get("user_name2")
            if not uname:
                continue
            scoreboard[game_type].setdefault(uname, {"wins": 0, "loses": 0, "draws": 0})
            scoreboard[game_type][uname]["wins"] += entry.get("wins", 0)
            scoreboard[game_type][uname]["loses"] += entry.get("loses", 0)
            scoreboard[game_type][uname]["draws"] += entry.get("draws", 0)
    else:
        raise ValueError(f"Неподдерживаемый тип игры: {game_type}")
    save_scoreboard(scoreboard)
