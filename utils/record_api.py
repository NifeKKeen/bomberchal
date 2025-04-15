import os
import json
from datetime import datetime

import globals
from pages.menu.play import get_setup_data_value
from utils.db_api import get_db_connection
from utils.helpers import players_sum_of_scores


GAME_LOGS_FILE = "game_logs.json"
# If cursor is specified in function arguments, it will use it
# to make CRUD operations on database

# 'on' suffix means online
# 'off' suffix means offline


def get_user_id_on(username, cursor=None):
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


def get_user_by_id_on(user_id, cursor):
    cursor.execute("SELECT username FROM users WHERE id = %s;", (user_id,))
    res = cursor.fetchone()
    if res:
        return res[0]
    raise Exception("User not found")


def access_username_on(username, cursor):
    cursor.execute("SELECT id FROM users WHERE username = %s;", (username,))
    return bool(cursor.fetchone())


def create_user_on(username, cursor):
    cursor.execute(
        """
        INSERT INTO
        users (username)
        VALUES (%s);
        """, (username,)
    )


def load_game_logs_off():
    if os.path.exists(GAME_LOGS_FILE):
        with open(GAME_LOGS_FILE, "r") as f:
            data = json.load(f)
    else:  # default null structure
        data = {
            "pve_games": [],
            "bossfight_games": [],
            "duel_games": []
        }

    # converting timestamps for each record in the lists
    for key in ("pve_games", "bossfight_games", "duel_games"):
        for record in data[key]:
            record["recorded_at"] = datetime.fromisoformat(record["recorded_at"])

    return data


def load_game_logs_on(cursor):
    game_logs = {
        "pve_games": [],
        "bossfight_games": [],
        "duel_games": []
    }

    cursor.execute(
        """
        SELECT users.username, p.score, p.recorded_at 
        FROM pve_games AS p 
        JOIN users ON p.user_id = users.id;
        """
    )
    for username, score, recorded_at in cursor.fetchall():
        game_logs["pve_games"].append({
            "username": username,
            "score": score,
            "recorded_at": recorded_at
        })

    cursor.execute(
        """
        SELECT users.username, b.score, b.recorded_at 
        FROM bossfight_games AS b 
        JOIN users ON b.user_id = users.id;
        """
    )
    for username, score, recorded_at in cursor.fetchall():
        game_logs["bossfight_games"].append({
            "username": username,
            "score": score,
            "recorded_at": recorded_at
        })

    cursor.execute(
        """
        SELECT users.username, d.wins, d.draws, d.loses, d.recorded_at 
        FROM duel_games AS d 
        JOIN users ON d.user_id = users.id;
        """
    )
    for username, wins, draws, loses, recorded_at in cursor.fetchall():
        game_logs["duel_games"].append({
            "username": username,
            "wins": wins,
            "draws": draws,
            "loses": loses,
            "recorded_at": recorded_at
        })

    return game_logs


def get_scoreboard_off():
    game_logs = load_game_logs_off()

    # Dictionary to accumulate user data.
    aggregated = {}

    for record in game_logs["pve_games"]:
        username = record["username"]
        score = record["score"]
        if username not in aggregated:
            aggregated[username] = {
                "username": username,
                "pve_score": 0,
                "bossfight_score": 0,
                "duel_wins": 0,
                "duel_loses": 0,
                "duel_draws": 0
            }
        aggregated[username]["pve_score"] += score

    for record in game_logs["bossfight_games"]:
        username = record["username"]
        score = record["score"]
        if username not in aggregated:
            aggregated[username] = {
                "username": username,
                "pve_score": 0,
                "bossfight_score": 0,
                "duel_wins": 0,
                "duel_loses": 0,
                "duel_draws": 0
            }
        aggregated[username]["bossfight_score"] += score

    for record in game_logs["duel_games"]:
        username = record["username"]
        wins = record["wins"]
        loses = record["loses"]
        draws = record["draws"]
        if username not in aggregated:
            aggregated[username] = {
                "username": username,
                "pve_score": 0,
                "bossfight_score": 0,
                "duel_wins": 0,
                "duel_loses": 0,
                "duel_draws": 0
            }
        aggregated[username]["duel_wins"] += wins
        aggregated[username]["duel_loses"] += loses
        aggregated[username]["duel_draws"] += draws

    return list(aggregated.values())


def save_game_logs_off(data):
    # converting datetime objects to ISO 8601 strings for JSON serialization
    def default(obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        raise TypeError(f"Save failed: Type {type(obj)} is not serializable")

    with open(GAME_LOGS_FILE, "w") as f:
        json.dump(data, f, indent=4, default=default)


def create_pve_record_on(username, score, cursor):
    if not access_username_on(username, cursor):
        create_user_on(username, cursor)
    cursor.execute(
        """
        INSERT INTO 
        pve_games (user_id, score)
        VALUES ((SELECT id FROM users WHERE username = %s), %s);
        """, (username, score)
    )


def create_bossfight_record_on(username, score, cursor):
    if not access_username_on(username, cursor):
        create_user_on(username, cursor)
    cursor.execute(
        """
        INSERT INTO 
        bossfight_games (user_id, score)
        VALUES ((SELECT id FROM users WHERE username = %s), %s);
        """, (username, score)
    )


def create_duels_record_on(username, wins, draws, loses, cursor):
    if not access_username_on(username, cursor):
        create_user_on(username, cursor)
    cursor.execute(
        """
        INSERT INTO 
        duel_games (user_id, wins, draws, loses)
        VALUES ((SELECT id FROM users WHERE username = %s), %s, %s, %s);
        """, (username, wins, loses, draws)
    )


def create_pve_record_off(username, score):
    data = load_game_logs_off()
    data["pve_games"].append({
        "username": username,
        "score": score,
        "recorded_at": datetime.now(),
    })
    save_game_logs_off(data)


def create_bossfight_record_off(username, score):
    data = load_game_logs_off()
    data["bossfight_games"].append({
        "username": username,
        "score": score,
        "recorded_at": datetime.now(),
    })
    save_game_logs_off(data)


def create_duels_record_off(username, wins, draws, loses):
    data = load_game_logs_off()
    data["duel_games"].append({
        "username": username,
        "wins": wins,
        "draws": draws,
        "loses": loses,
        "recorded_at": datetime.now(),
    })
    save_game_logs_off(data)


def record_game(data, online=False):  # API endpoint
    game_mode = data["game_mode"]
    player_cnt = get_setup_data_value("players")

    if online:
        db = get_db_connection(True)
        db_cursor = db.cursor()

        if game_mode == "pve":
            # expecting data["payload"] to be compatible what players_sum_of_scores receives
            score = players_sum_of_scores(data["payload"])
            for idx in range(player_cnt):
                if not len(globals.usernames[idx]):  # username is not set
                    continue

                create_pve_record_on(globals.usernames[idx], score, db_cursor)
        elif game_mode == "bossfight":
            # expecting data["payload"] to be compatible what players_sum_of_scores receives
            score = players_sum_of_scores(data["payload"])
            for idx in range(player_cnt):
                if not len(globals.usernames[idx]):  # username is not set
                    continue

                create_bossfight_record_on(globals.usernames[idx], score, db_cursor)
        elif game_mode == "duel":
            # expecting data["payload"] to be id of the game player (NOT user_id)
            for idx in range(player_cnt):
                if not len(globals.usernames[idx]):  # username is not set
                    continue
                print("Saving data for", idx, globals.usernames[idx])
                if data["payload"] == -1:  # draw
                    create_duels_record_on(
                        globals.usernames[idx],
                        0, 1, 0,
                        db_cursor
                    )
                elif idx + 1 == data["payload"]:  # winner
                    create_duels_record_on(
                        globals.usernames[idx],
                        1, 0, 0,
                        db_cursor
                    )
                else:  # loser
                    create_duels_record_on(
                        globals.usernames[idx],
                        0, 0, 1,
                        db_cursor
                    )
        else:
            raise "Unknown game mode"

        db.commit()
        db_cursor.close()
    else:
        if game_mode == "pve":
            # expecting data["payload"] to be compatible what players_sum_of_scores receives
            score = players_sum_of_scores(data["payload"])
            for idx in range(player_cnt):
                if not len(globals.usernames[idx]):  # username is not set
                    continue

                create_pve_record_off(globals.usernames[idx], score)
        elif game_mode == "bossfight":
            # expecting data["payload"] to be compatible what players_sum_of_scores receives
            score = players_sum_of_scores(data["payload"])
            for idx in range(player_cnt):
                if not len(globals.usernames[idx]):  # username is not set
                    continue

                create_bossfight_record_off(globals.usernames[idx], score)
        elif game_mode == "duel":
            # expecting data["payload"] to be id of the game player (NOT user_id)
            for idx in range(player_cnt):
                if not len(globals.usernames[idx]):  # username is not set
                    continue
                if data["payload"] == -1:  # draw
                    create_duels_record_off(
                        globals.usernames[idx],
                        0, 1, 0,
                    )
                elif idx + 1 == data["payload"]:  # winner
                    create_duels_record_off(
                        globals.usernames[idx],
                        1, 0, 0,
                    )
                else:  # loser
                    create_duels_record_off(
                        globals.usernames[idx],
                        0, 0, 1,
                    )
        else:
            raise "Unknown game mode"


if __name__ == "__main__":
    print(load_game_logs_on(get_db_connection().cursor()))
