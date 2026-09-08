import requests

url = "https://api.nhle.com/stats/rest/en/skater/summary"

params = {
    "limit": 10,
    "cayenneExp": "seasonId=20252026 and gameTypeId=2"
}

response = requests.get(url, params=params)

print("Status code:", response.status_code)

data = response.json()

for player in data["data"]:
    print(player["skaterFullName"], "-", player["points"], "points")