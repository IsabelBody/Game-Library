from games.adapters.database_repository import SqlAlchemyRepository
from games.adapters.datareader.csvdatareader import GameFileCSVReader
import os
from pathlib import Path
from games.adapters.repository import AbstractRepository


def populate(data_path: Path, repo: SqlAlchemyRepository, database_mode: bool):
    games_file_name = str(data_path / "games.csv")

    reader = GameFileCSVReader(games_file_name)

    reader.read_csv_file()

    publishers = reader.dataset_of_publishers
    games = reader.dataset_of_games

    genres = reader.dataset_of_genres

    # Add publishers to the repo
    for publisher in publishers:
        repo.add_publisher(publisher)

    # Add genres to the repo
    for genre in genres:
        repo.add_genre(genre)

    # Add games to the repo
    for game in games:
        repo.add_game(game)

    # Commit changes to the database if using SQLAlchemy sessions
    if database_mode == True:
        repo.commit()
