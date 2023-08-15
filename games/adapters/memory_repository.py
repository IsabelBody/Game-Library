import csv
import os.path
from pathlib import Path
from typing import List
from games import *
from games.adapters.repository import AbstractRepository, RepositoryException
# importing classes from model.
from games.domainmodel.model import Publisher, Genre, User, Game, User, Review
# importing datareader
from games.adapters.datareader.csvdatareader import *
from bisect import bisect, bisect_left, insort_left

class MemoryRepository(AbstractRepository):
    def __init__(self):
        # starting with just games
        self.__games = list()

    # getters and setters
    def add_game(self, game: Game):
        if isinstance(game, Game):
            insort_left(self.__games, game)

    def get_games(self) -> List[Game]:
        return self.__games

    def get_number_of_games(self):
        return len(self.__games)

def populate(repo: AbstractRepository):
    dir_name = os.path.dirname(os.path.abspath(__file__))
    games_file_name = os.path.join(dir_name, "data/games.csv")
    reader = GameFileCSVReader(games_file_name)
    reader.read_csv_file()
    games = reader.dataset_of_games

    # add games to the repo
    for game in games:
        repo.add_game(game)

