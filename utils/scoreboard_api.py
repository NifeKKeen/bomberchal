import os
import json

import globals
from pages.menu.play import get_setup_data_value
from utils.db_api import get_db_connection
from utils.helpers import players_sum_of_scores


SCOREBOARD_FILE = "utils/scoreboard.json"
# If cursor is specified in function arguments, it will use it
# to make CRUD operations on database

def get_user_id(username, cursor=None):
    if cursor is None:
        # in offline mode, there are no integer keys, so user_id will actually be username
        return username

    try:
        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        res = cursor.fetchone()
        if res:
            return int(res[0])
        cursor.execute("SELECT COUNT(*) + 1 FROM users")
        id = cursor.fetchone()[0]
        cursor.execute("INSERT INTO users (username) VALUES (%s)", (username,))
        return id
    except Exception as e:
        print(e)

def get_user_by_id(user_id, cursor=None):
    if cursor is None:
        # in offline mode, there are no integer keys, so user_id will actually be username
        return user_id

    try:
        cursor.execute("SELECT username FROM users WHERE id = %s", (user_id,))
        res = cursor.fetchone()
        if res:
            return res[0]
        raise Exception("user not found")
    except Exception as e:
        print(e)
    return None



def _load_scoreboard_data(cursor=None):
    data = {"scoreboard": []}

    try:
        if cursor is None:
            raise Exception("Cursor is not provided")
        # online data is available
        try:
            cursor.execute("SELECT * FROM scoreboard")
            print("EXECUTE")
        except Exception as e:
            print(e, "OSHIBKA")

        for row in cursor.fetchall():
            data["scoreboard"].append({
                "username": get_user_by_id(row[0]),
                "pve_score": row[1],
                "bossfight_score": row[2],
                "duel_wins": row[3],
                "duel_loses": row[4],
                "duel_draws": row[5],
            })

        _save_scoreboard_data(data) # saving into scoreboard

        return data

    except Exception as e:  # switching to offline data
        print("_load_scoreboard_data", e)
        if not os.path.exists(SCOREBOARD_FILE):
            with open(SCOREBOARD_FILE, 'w') as f:
                json.dump(data, f, indent=4)
        else:
            with open(SCOREBOARD_FILE, 'r') as f:
                try:
                    data = json.load(f)
                except:
                    data = {"scoreboard": []}
        return data


def _save_scoreboard_data(data):
    with open(SCOREBOARD_FILE, 'w') as f:
        json.dump(data, f, indent=4)


def get_scoreboard(mode):
    mode = mode.lower()

    try:
        db = get_db_connection()

        if db is None:
            raise Exception("No connection to db")
        with db.cursor() as cursor:
            data = _load_scoreboard_data(cursor=cursor)
    except Exception as e: # offline mode
        print("ERROR get_scoreboard", e)
        data = _load_scoreboard_data()
        print("DATA", data)

    scoreboard_list = data.get("scoreboard", [])
    # data is already scoreboard
    if mode in ("pve", "bossfight"):
        sorted_list = sorted(
            scoreboard_list,
            key=lambda x: x.get(f"{mode}_score", 0),
            reverse=True
        )
    elif mode == "duel":
        sorted_list = sorted(
            scoreboard_list,
            key=lambda x: (x.get("duel_wins", 0),
                           -x.get("duel_loses", 0)),
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
    user_id = get_user_id(username, cursor=cursor)

    for entry in data:
        if entry.get("username") == username:
            if cursor: # online
                if f"{mode}_score" not in entry:
                    try:
                        cursor.execute(f'UPDATE scoreboard SET {mode}_score = %s WHERE user_id = %s', (0, user_id))
                    except Exception as e:
                        print(e)
                if score > entry.get(f"{mode}_score", 0):
                    try:
                        cursor.execute(f'UPDATE scoreboard SET {mode}_score = %s WHERE user_id = %s', (score, user_id))
                    except Exception as e:
                        print(e)

            else: # offline
                if mode not in entry:
                    entry = {f"{mode}_score": 0}
                if score > entry.get("score", 0):
                    entry[f"{mode}_score"] = score

            updated = True
            break

    if not updated:  # inserting new entry
        if cursor:
            pve_score = score if mode == "pve" else 0
            bossfight_score = score if mode == "bossfight" else 0
            try:
                cursor.execute("""
                    INSERT INTO scoreboard (user_id, pve_score, bossfight_score, duel_wins, duel_loses, duel_draws)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (user_id, pve_score, bossfight_score, 0, 0, 0))
            except Exception as e:
                print(e)
        else:
            new_entry = {
                "username": username,
                "pve_score": score if mode == "pve" else 0,
                "bossfight": score if mode == "bossfight" else 0,
                "duel_wins": 0,
                "duel_loses": 0,
                "duel_draws": 0
            }
            data.append(new_entry)
    _save_scoreboard_data(data)


def _update_duel(username, wins=0, loses=0, draws=0, cursor=None):
    data = _load_scoreboard_data(cursor=cursor)
    found = False
    user_id = get_user_id(username, cursor=cursor)

    for entry in data:
        if entry.get("username") == username:
            if cursor:
                cursor.execute("""UPDATE scoreboard SET duel_wins = duel_wins + %s, duel_loses = duel_loses + %s,
                duel_draws = duel_draws + %s WHERE user_id = %s""", (wins, loses, draws, user_id))
            else:
                entry["duel_wins"] += wins
                entry["duel_loses"] += loses
                entry["duel_draws"] += draws
            found = True
            break
    if not found:  # inserting new entry
        if cursor:
            cursor.execute("""INSERT INTO scoreboard (user_id, pve_score, bossfight_score,
            duel_wins, duel_loses, duel_draws) VALUES (%s, %s, %s, %s, %s, %s)""", (user_id, 0, 0, wins, loses, draws))
        else:
            new_entry = {
                "username": username,
                "pve_score": 0,
                "bossfight_score": 0,
                "duel_wins": 0,
                "duel_loses": 0,
                "duel_draws": 0
            }
            data["scoreboard"].append(new_entry)
    _save_scoreboard_data(data)


def save_data(data):  # API endpoint
    db_cursor = None
    try:  # online
        db = get_db_connection()
        if not db:
            raise Exception("No db connection")
        db_cursor = db.cursor()
        # with db.cursor() as cursor:
        #     db_cursor = cursor
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

    if db_cursor is not None:
        db_cursor.connection.commit()
        db_cursor.close()
