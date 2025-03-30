import os
import json
import globals

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
