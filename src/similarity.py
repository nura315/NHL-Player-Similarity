import sqlite3
import pandas as pd

from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity


DATABASE = "data/nhl.db"

# -------------------------
# 1. LOAD DATA
# -------------------------

conn = sqlite3.connect(DATABASE)

query = """
SELECT
    player_name,
    team,
    positionCode,
    games_played,
    goals,
    assists,
    shots,
    penaltyMinutes,
    ppPoints,
    even_strength_points,
    shootingPct,
    time_on_ice_per_game
FROM skater_stats
WHERE games_played >= 20;
"""

df = pd.read_sql_query(query, conn)

conn.close()


# -------------------------
# 2. CREATE FEATURES
# -------------------------

# NHL gives average time on ice in seconds.
# Estimate each player's total ice time in minutes.
df["total_minutes"] = (
    df["time_on_ice_per_game"]
    * df["games_played"]
    / 60
)

# Production rate per 60 minutes of ice time
df["goals_per_60"] = (
    df["goals"]
    / df["total_minutes"]
    * 60
)

df["assists_per_60"] = (
    df["assists"]
    / df["total_minutes"]
    * 60
)

df["shots_per_60"] = (
    df["shots"]
    / df["total_minutes"]
    * 60
)

df["pp_points_per_60"] = (
    df["ppPoints"]
    / df["total_minutes"]
    * 60
)

df["ev_points_per_60"] = (
    df["even_strength_points"]
    / df["total_minutes"]
    * 60
)

df["pim_per_60"] = (
    df["penaltyMinutes"]
    / df["total_minutes"]
    * 60
)


features = [
    "goals_per_60",
    "assists_per_60",
    "shots_per_60",
    "pp_points_per_60",
    "ev_points_per_60",
    "shootingPct",
    "pim_per_60",
    "time_on_ice_per_game"
]


# -------------------------
# 3. STANDARDIZE FEATURES
# -------------------------

X = df[features].copy()

# Fill missing values with each column's median
X = X.fillna(X.median())

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)


# -------------------------
# 4. CALCULATE SIMILARITY
# -------------------------

similarity_matrix = cosine_similarity(
    X_scaled
)


# -------------------------
# 5. FIND SIMILAR PLAYERS
# -------------------------

def find_similar_players(player_name, n=5):

    matches = df[
        df["player_name"].str.lower()
        == player_name.lower()
    ]

    if matches.empty:
        return None, None

    player_index = matches.index[0]

    player_position = df.loc[
        player_index,
        "positionCode"
    ]

    scores = []

    for index in df.index:

        if index == player_index:
            continue

        # Only compare players at the same position
        if df.loc[index, "positionCode"] != player_position:
            continue

        score = similarity_matrix[
            player_index,
            index
        ]

        scores.append(
            (index, score)
        )

    scores = sorted(
        scores,
        key=lambda x: x[1],
        reverse=True
    )[:n]

    results = []

    for index, score in scores:

        player = df.loc[index]

        results.append({
            "player_name": player["player_name"],
            "team": player["team"],
            "position": player["positionCode"],
            "cosine_score": score,
            "goals_per_60": player["goals_per_60"],
            "assists_per_60": player["assists_per_60"],
            "shots_per_60": player["shots_per_60"],
            "shooting_pct": player["shootingPct"],
            "pp_points_per_60": player["pp_points_per_60"],
            "ev_points_per_60": player["ev_points_per_60"]
        })

    return player_position, results

def get_player_stats(player_name):

    matches = df[
        df["player_name"].str.lower()
        == player_name.lower()
    ]

    if matches.empty:
        return None

    player = matches.iloc[0]

    return {
        "player_name": player["player_name"],
        "goals_per_60": player["goals_per_60"],
        "assists_per_60": player["assists_per_60"],
        "shots_per_60": player["shots_per_60"],
        "shooting_pct": player["shootingPct"],
        "pp_points_per_60": player["pp_points_per_60"],
        "ev_points_per_60": player["ev_points_per_60"]
    }

def get_position_percentiles(player_name):

    matches = df[
        df["player_name"].str.lower()
        == player_name.lower()
    ]

    if matches.empty:
        return None

    player = matches.iloc[0]
    position = player["positionCode"]

    position_df = df[
        df["positionCode"] == position
    ]

    metrics = [
        "goals_per_60",
        "assists_per_60",
        "shots_per_60",
        "shootingPct"
    ]

    percentiles = {}

    for metric in metrics:

        percentile = (
            position_df[metric]
            .rank(pct=True)
            .loc[player.name]
            * 100
        )

        percentiles[metric] = percentile

    return percentiles