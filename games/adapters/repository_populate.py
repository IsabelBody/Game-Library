from games.adapters.datareader.csvdatareader import GameFileCSVReader
import os
from pathlib import Path
from games.adapters.repository import AbstractRepository

def populate(data_path: Path, repo: AbstractRepository):
    games_file_name = str(data_path / "games.csv")

    reader = GameFileCSVReader(games_file_name)

    reader.read_csv_file()

    publishers = reader.dataset_of_publishers
    games = reader.dataset_of_games
    genres = reader.dataset_of_genres

    # Add publishers to the repo
    repo.add_publisher(publishers)

    # Add genres to the repo
    repo.add_genre(genres)

    # Add games to the repo
    repo.add_game(games)

    # Commit changes to the database if using SQLAlchemy sessions
    repo.commit()
