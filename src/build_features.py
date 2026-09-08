import sqlite3
import pandas as pd

DATABASE = "data/nhl.db"

conn = sqlite3.connect(DATABASE)

query = """
SELECT
    player_name,
    team,
    games_played,
    goals,
    assists,
    points,
    shots,
    penaltyMinutes,
    ppPoints
FROM skater_stats
WHERE games_played >= 20;
"""

df = pd.read_sql_query(query, conn)

conn.close()

df["goals_per_game"] = df["goals"] / df["games_played"]
df["assists_per_game"] = df["assists"] / df["games_played"]
df["points_per_game"] = df["points"] / df["games_played"]
df["shots_per_game"] = df["shots"] / df["games_played"]
df["pim_per_game"] = df["penaltyMinutes"] / df["games_played"]
df["pp_points_per_game"] = df["ppPoints"] / df["games_played"]

print(
    df[
        [
            "player_name",
            "team",
            "goals_per_game",
            "assists_per_game",
            "points_per_game",
            "shots_per_game",
            "pim_per_game",
            "pp_points_per_game",
        ]
    ].head(10)
)