#something

def add_payload(user_name, game_type, payload):
    if game_type in ("pve", "bossfight"):
        if payload.get("user_name") != user_name:
            raise ValueError("Имя пользователя в payload не соответствует переданному значению.")
        value = payload.get("value", 0)
        if user_name not in globals.scoreboard[game_type]:
            globals.scoreboard[game_type][user_name] = 0
        globals.scoreboard[game_type][user_name] += value
    elif game_type == "duel":
        for entry in payload:
            if "user_name1" in entry:
                uname = entry["user_name1"]
            elif "user_name2" in entry:
                uname = entry["user_name2"]
            else:
                continue

            if uname not in globals.scoreboard[game_type]:
                globals.scoreboard[game_type][uname] = {"wins": 0, "loses": 0, "draws": 0}
            
            globals.scoreboard[game_type][uname]["wins"] += entry.get("wins", 0)
            globals.scoreboard[game_type][uname]["loses"] += entry.get("loses", 0)
            globals.scoreboard[game_type][uname]["draws"] += entry.get("draws", 0)
        else:
            raise ValueError(f"Неподдерживаемый тип игры: {game_type}")