import os
import sqlite3
import pandas as pd
import streamlit as st
import altair as alt

from src.load import load_data

DATABASE = "data/nhl.db"

if not os.path.exists(DATABASE):
    load_data()

from src.similarity import (
    find_similar_players,
    get_player_stats,
    get_position_percentiles
)


# -------------------------
# PAGE SETUP
# -------------------------

st.title("🏒 NHL Player Similarity Explorer")

st.write(
    "Find NHL players with similar statistical profiles."
)


# -------------------------
# LOAD PLAYERS
# -------------------------

conn = sqlite3.connect(DATABASE)

query = """
SELECT
    player_name,
    team,
    positionCode,
    games_played
FROM skater_stats
WHERE games_played >= 20
ORDER BY player_name;
"""

df = pd.read_sql_query(query, conn)

conn.close()


# -------------------------
# PLAYER DROPDOWN
# -------------------------

player_names = df["player_name"].tolist()

selected_player = st.selectbox(
    "Choose an NHL player:",
    player_names
)


# -------------------------
# DISPLAY SELECTION
# -------------------------

player = df[
    df["player_name"] == selected_player
].iloc[0]

st.subheader(selected_player)

st.write(f"Team: {player['team']}")
st.write(f"Position: {player['positionCode']}")
st.write(f"Games played: {player['games_played']}")

# -------------------------
# SIMILAR PLAYERS
# -------------------------

position, similar_players = find_similar_players(
    selected_player
)

st.subheader(
    f"Most similar players at position {position}"
)

results_df = pd.DataFrame(similar_players)

results_df["cosine_score"] = results_df[
    "cosine_score"
].round(3)

results_df["goals_per_60"] = results_df[
    "goals_per_60"
].round(2)

results_df["assists_per_60"] = results_df[
    "assists_per_60"
].round(2)

results_df["shots_per_60"] = results_df[
    "shots_per_60"
].round(2)

results_df["shooting_pct"] = (
    results_df["shooting_pct"] * 100
).round(1)

results_df = results_df.rename(columns={
    "player_name": "Player",
    "team": "Team",
    "position": "Position",
    "cosine_score": "Cosine Score",
    "goals_per_60": "Goals / 60 TOI",
    "assists_per_60": "Assists / 60 TOI",
    "shots_per_60": "Shots / 60 TOI",
    "shooting_pct": "Shooting %"
})

display_columns = [
    "Player",
    "Team",
    "Position",
    "Cosine Score",
    "Goals / 60 TOI",
    "Assists / 60 TOI",
    "Shots / 60 TOI",
    "Shooting %"
]

results_display = results_df[
    display_columns
]

st.dataframe(
    results_display,
    hide_index=True,
    width="stretch"
)


st.caption(
    "TOI = Time on Ice. Per-60 TOI stats measure production "
    "for every 60 minutes a player is actually on the ice."
)


# -------------------------
# TOP MATCH COMPARISON
# -------------------------

selected_stats = get_player_stats(
    selected_player
)

comparison_options = [
    player["player_name"]
    for player in similar_players
]

comparison_player = st.selectbox(
    "Compare with:",
    comparison_options
)

comparison_match = next(
    player
    for player in similar_players
    if player["player_name"] == comparison_player
)

top_match = comparison_match

st.subheader(
    f"{selected_player} vs. "
    f"{top_match['player_name']}"
)

comparison_df = pd.DataFrame({
    "Stat": [
        "Goals / 60 TOI",
        "Assists / 60 TOI",
        "Shots / 60 TOI",
        "Shooting %"
    ],

    selected_player: [
        selected_stats["goals_per_60"],
        selected_stats["assists_per_60"],
        selected_stats["shots_per_60"],
        selected_stats["shooting_pct"] * 100
    ],

    top_match["player_name"]: [
        top_match["goals_per_60"],
        top_match["assists_per_60"],
        top_match["shots_per_60"],
        top_match["shooting_pct"] * 100
    ]
})

comparison_df[
    [selected_player, top_match["player_name"]]
] = comparison_df[
    [selected_player, top_match["player_name"]]
].round(2)

st.dataframe(
    comparison_df,
    hide_index=True,
    width="stretch"
)


# -------------------------
# PERCENTILE COMPARISON
# -------------------------

selected_percentiles = get_position_percentiles(
    selected_player
)

match_percentiles = get_position_percentiles(
    top_match["player_name"]
)

chart_df = pd.DataFrame({
    selected_player: [
        selected_percentiles["goals_per_60"],
        selected_percentiles["assists_per_60"],
        selected_percentiles["shots_per_60"],
        selected_percentiles["shootingPct"]
    ],

    top_match["player_name"]: [
        match_percentiles["goals_per_60"],
        match_percentiles["assists_per_60"],
        match_percentiles["shots_per_60"],
        match_percentiles["shootingPct"]
    ]
},
index=[
    "Goals / 60 TOI",
    "Assists / 60 TOI",
    "Shots / 60 TOI",
    "Shooting %"
])

st.subheader("Statistical Profile")

st.caption(
    "Percentile rank compared with other players "
    "at the same position."
)

chart_data = (
    chart_df
    .reset_index()
    .rename(columns={"index": "Stat"})
    .melt(
        id_vars="Stat",
        var_name="Player",
        value_name="Percentile"
    )
)

chart = alt.Chart(chart_data).mark_bar().encode(
    x=alt.X(
        "Stat:N",
        title=None,
        sort=[
            "Goals / 60 TOI",
            "Assists / 60 TOI",
            "Shots / 60 TOI",
            "Shooting %"
        ]
    ),
    xOffset="Player:N",

    y=alt.Y(
        "Percentile:Q",
        title="Percentile",
        scale=alt.Scale(
            domain=[0, 100]
        )
    ),

    color=alt.Color(
        "Player:N",
        title="Player"
    ),

    tooltip=[
        "Player:N",
        "Stat:N",
        alt.Tooltip(
            "Percentile:Q",
            format=".1f"
        )
    ]
)

st.altair_chart(
    chart,
    width="stretch"
)