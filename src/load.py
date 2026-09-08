import sqlite3

from extract_nhl import get_skater_summary


DATABASE = "data/nhl.db"
SEASON = 20252026


def load_data():
    df = get_skater_summary(SEASON)

    df = df.rename(columns={
        "skaterFullName": "player_name",
        "teamAbbrevs": "team",
        "gamesPlayed": "games_played",
        "gameWinningGoals": "game_winning_goals",
        "faceoffWinPct": "faceoff_win_pct",
        "shootsCatches": "shoots_catches",
        "timeOnIcePerGame": "time_on_ice_per_game",
        "evGoals": "even_strength_goals",
        "evPoints": "even_strength_points"
    })

    conn = sqlite3.connect(DATABASE)

    df.to_sql(
        "skater_stats",
        conn,
        if_exists="replace",
        index=False
    )

    conn.close()

    print(f"Loaded {len(df)} rows into {DATABASE}")


if __name__ == "__main__":
    load_data()