import os
import json

import psycopg2

import globals
from pages.menu.play import get_setup_data_value
from utils.db_api import get_db_connection
from utils.helpers import players_sum_of_scores


SCOREBOARD_FILE = "utils/scoreboard.json"
# If cursor is specified in function arguments, it will use it
# to make CRUD operations on database


def _load_scoreboard_data(cursor=None):
    try:
        if cursor is None:
            raise Exception("Cursor is not provided")
        # online data is available
        print("Loading scoreboard data")
        try:
            cursor.execute("SELECT * FROM scoreboard")
        except Exception as e:
            print(e, "OSHIBKA")
        data = {"scoreboard": []}
        for row in cursor.fetchall():
            data["scoreboard"].append(dict(row))

    except: # switching to offline data
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



def _save_scoreboard_data(data):
    with open(SCOREBOARD_FILE, 'w') as f:
        json.dump(data, f, indent=4)


def get_scoreboard(mode, cursor=None):
    mode = mode.lower()
    data = _load_scoreboard_data(cursor=cursor)
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


def update_score(mode, username, score, cursor=None):
    mode = mode.lower()
    if mode not in ("pve", "bossfight"):
        raise ValueError("update only for pve or bossfight modes.")
    data = _load_scoreboard_data(cursor=cursor)
    updated = False
    for entry in data["scoreboard"]:
        if entry.get("username") == username:
            if cursor: # online
                if mode not in entry:
                    try:
                        cursor.execute(f"UPDATE scoreboard SET {mode}_score = 0 WHERE username = {username}")
                    except Exception as e:
                        print(e)
                if score > entry[mode].get("score", 0):
                    try:
                        cursor.execute(f"UPDATE scoreboard SET {mode}_score = {score} WHERE username = {username}")
                    except Exception as e:
                        print(e)

            else: # offline
                if mode not in entry:
                    entry[mode] = {"score": 0}
                if score > entry[mode].get("score", 0):
                    entry[mode]["score"] = score

            updated = True
            break

    if not updated:
        if cursor:
            pve_score = {"score": score} if mode == "pve" else {"score": 0}
            bossfight_score = {"score": score} if mode == "bossfight" else {"score": 0}
            duel_wins = {"score": score} if mode == "pve" else {"score": 0}
            duel_losses = {"score": score} if mode == "pve" else {"score": 0}
            duel_draws = {"score": score} if mode == "pve" else {"score": 0}
            try:
                cursor.execute(f"INSERT INTO scoreboard VALUES pve_score = {pve_score}, bossfight_score = {bossfight_score},"
                           f"duel_wins = {duel_wins}, duel_losses = {duel_losses}, duel_draws = {duel_draws} WHERE username = {username}")
            except Exception as e:
                print(e)
        else:
            new_entry = {
                "username": username,
                "pve": {"score": score} if mode == "pve" else {"score": 0},
                "bossfight": {"score": score} if mode == "bossfight" else {"score": 0},
                "duel": {"wins": 0, "losses": 0, "draws": 0}
            }
            data["scoreboard"].append(new_entry)
    _save_scoreboard_data(data)
    return get_scoreboard(mode, cursor=cursor)


def _update_duel(username, wins=0, losses=0, draws=0, cursor=None):
    if cursor:
        pass
    else:
        data = _load_scoreboard_data(cursor=cursor)
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
        _save_scoreboard_data(data)
        return get_scoreboard("duel", cursor=cursor)


def save_data(data):  # API endpoint
    db_cursor = None
    try:  # online
        db = get_db_connection()
        db_cursor = db.cursor()
        # with db.cursor() as cursor:
        #     db_cursor = cursor
        print("Online!")
    except Exception as e:  # offline
        print(e)


    game_mode = data["game_mode"]
    player_cnt = get_setup_data_value("players")
    if game_mode == "duel":
        for idx in range(player_cnt):
            if not len(globals.usernames[idx]):
                continue

            if data["payload"] == -1:  # draw
                _update_duel(
                    globals.usernames[idx],
                    0, 0, 1,
                    db_cursor
                )
            elif idx + 1 == data["payload"]:  # winner
                _update_duel(
                    globals.usernames[idx],
                    1, 0, 0,
                    db_cursor
                )
            else:
                _update_duel(
                    globals.usernames[idx],
                    0, 1, 0,
                    db_cursor
                )
    elif game_mode == "pve" or game_mode == "bossfight":
        score = players_sum_of_scores(data["payload"])
        for idx in range(player_cnt):
            if not len(globals.usernames[idx]):
                continue

            print(db_cursor)
            update_score(game_mode, globals.usernames[idx], score, db_cursor)
