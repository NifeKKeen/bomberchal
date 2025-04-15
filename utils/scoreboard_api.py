def get_processed_score_data(score_data, game_mode):
    # score_data it is what get_accumulated_scores_off or get_accumulated_scores_on return

    if game_mode == "pve":
        sort_key = "pve_score"
    elif game_mode == "bossfight":
        sort_key = "bossfight_score"
    elif game_mode == "duel":
        sort_key = "duel_wins"
    else:
        raise f"Unsupported game_mode: {game_mode}"

    sorted_data = sorted(score_data, key=lambda user: user[sort_key], reverse=True)

    return sorted_data[:5]
