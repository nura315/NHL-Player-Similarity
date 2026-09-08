import requests
import pandas as pd

BASE_URL = "https://api.nhle.com/stats/rest/en"


def get_skater_summary(season, game_type=2):
    url = f"{BASE_URL}/skater/summary"

    params = {
        "limit": -1,
        "cayenneExp": f"seasonId={season} and gameTypeId={game_type}"
    }

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()

    data = response.json()

    return pd.DataFrame(data["data"])


if __name__ == "__main__":
    df = get_skater_summary(20252026)

    print(df.shape)
    print(df.head())