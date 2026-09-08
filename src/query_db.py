import sqlite3
import pandas as pd

DATABASE = "data/nhl.db"

conn = sqlite3.connect(DATABASE)

query = """
SELECT
    player_name,
    time_on_ice_per_game
FROM skater_stats
ORDER BY points DESC
LIMIT 10;
"""

df = pd.read_sql_query(query, conn)

conn.close()

print(df)