# NHL Player Similarity Explorer 🏒

An interactive NHL analytics application that finds statistically similar players based on their on-ice production.

The project collects NHL skater statistics, stores the data in a SQLite database, creates rate-based features, and uses cosine similarity to compare players at the same position.

The results are displayed in an interactive Streamlit application where users can select a player, view their closest statistical matches, and compare their statistical profiles.

## How It Works

1. NHL skater statistics are retrieved from the NHL API.
2. The data is cleaned and stored in a SQLite database.
3. Player statistics are converted into rate statistics, including goals, assists, and shots per 60 minutes of time on ice (TOI).
4. Features are standardized using `StandardScaler`.
5. Cosine similarity is used to compare each player with other players at the same position.
6. The most similar players are displayed in an interactive Streamlit dashboard.

## Similarity Features

The similarity model currently considers:

- Goals per 60 minutes of time on ice
- Assists per 60 minutes of time on ice
- Shots per 60 minutes of time on ice
- Power-play points relative to total time on ice
- Even-strength points relative to total time on ice
- Shooting percentage
- Penalty minutes per 60 minutes of time on ice
- Average time on ice per game

Only players at the same position are compared.

Players must have played at least 20 games to be included in the analysis.

## Tech Stack

- Python
- pandas
- scikit-learn
- SQLite
- Streamlit
- Altair
- NHL public API

## Project Structure

```text
NHL-Player-Similarity/
├── data/
│   └── nhl.db
├── src/
│   ├── extract_nhl.py
│   ├── load.py
│   ├── similarity.py
│   └── test_api.py
├── app.py
├── requirements.txt
└── README.md
```

## Running the Project

Create and activate a Python virtual environment, install the dependencies, load the NHL data, and start the Streamlit application.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/load.py
streamlit run app.py
```

Then open the local Streamlit URL shown in the terminal.

## Methodology

Player similarity is calculated using standardized statistical features and cosine similarity.

Before calculating similarity, player statistics are converted into rate-based features. For example, goals per 60 minutes of time on ice measures a player's scoring rate based on how much time they actually spend on the ice rather than simply how many games they have played.

The features are then standardized using scikit-learn's `StandardScaler`. Standardization puts features measured on different scales onto a comparable scale so that a feature with larger numerical values does not automatically have a larger influence on the comparison.

Cosine similarity is then calculated between players' standardized feature vectors. Players are only compared with other players at the same position.

The cosine score is used as a ranking metric. It should not be interpreted as a percentage probability that two players are similar.

## Statistical Profile

The Streamlit application also displays percentile-based statistical profiles for player comparisons.

Percentile ranks show how a player performs in a statistic relative to other eligible players at the same position. For example, a player in the 90th percentile for goals per 60 minutes has a higher goals-per-60 rate than approximately 90% of the eligible players at that position in the dataset.

## Data

The current version uses NHL skater statistics from the 2025-26 regular season.

The data is retrieved from the NHL's public-facing statistics API and loaded into a local SQLite database.

Only skaters with at least 20 games played are included in the similarity analysis to reduce the effect of very small sample sizes.

## Future Improvements

Potential future improvements include:

- Support for multiple NHL seasons
- Additional player filters
- Improved handling of special-teams statistics using power-play-specific time on ice
- Additional similarity features
- Expanded player comparison visualizations