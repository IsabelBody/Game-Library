import csv
import os.path
from pathlib import Path
from typing import List
from games import *
from games.adapters.repository import AbstractRepository, RepositoryException
from games.domainmodel.model import Publisher, Genre, User, Game, User, Review, Wishlist
from games.adapters.datareader.csvdatareader import *
from bisect import bisect, bisect_left, insort_left


class MemoryRepository(AbstractRepository):
    def __init__(self):
        # starting with just games
        self.__games = list()
        self.__genres = list()
        self.__publishers = list()

        # for the login stuff
        self.__users = list()
        self.__wishlists = list()

    def add_user(self, user: User):
        self.__users.append(user)

    def get_user(self, user_name) -> User:
        return next((user for user in self.__users if user.username == user_name), None)

    # methods for wishlist
    def add_wishlist(self, user: User):
        wishlist = Wishlist(user)
        self.__wishlists.append(wishlist)
        return wishlist

    def get_wishlists(self):
        return self.__wishlists

    def add_wishlist_game(self, user: User, game: Game):
        if isinstance(user, User) and isinstance(game, Game):
            user_wishlist = next(
                (wishlist for wishlist in self.__wishlists if wishlist.user == user), None)
            if user_wishlist == None:
                user_wishlist = self.add_wishlist(user)

            if game not in user_wishlist.list_of_games():
                user_wishlist.add_game(game)

    def get_wishlist_games(self, user) -> List[Game]:
        if isinstance(user, User):
            user_wishlist = next(
                (wishlist for wishlist in self.__wishlists if wishlist.user == user), None)
            return user_wishlist.list_of_games()
        else:
            return None

    def remove_wishlist_game(self, user: User, game: Game):
        user_wishlist = next(
            (wishlist for wishlist in self.__wishlists if wishlist.user == user), None)

        if user_wishlist is not None:
            if game in user_wishlist.list_of_games():
                user_wishlist.remove_game(game)
                return True

        return False

    # getters and setters

    def add_game(self, game: Game):
        if isinstance(game, Game):
            insort_left(self.__games, game)

    def get_game(self, game_id) -> Game:
        for game in self.__games:
            if game.game_id == game_id:
                return game
        return "Error not found"

    def get_games(self) -> List[Game]:
        return self.__games

    def add_genre(self, genre: Genre):
        if isinstance(genre, Genre):
            insort_left(self.__genres, genre)

    def get_genre(self) -> List[Genre]:
        return self.__genres

    def get_number_of_games(self):
        return len(self.__games)

    def get_number_of_unique_genres(self):
        return len(self.__genres)

    def get_games_for_genre(self, genre_name):
        matching_games = []

        for game in self.__games:
            if genre_name.lower() in [genre.genre_name.lower() for genre in game.genres]:
                matching_games.append(game)
        return matching_games

    def add_publisher(self, publisher: Publisher):
        if isinstance(publisher, Publisher):
            insort_left(self.__publishers, publisher)

    def get_publishers(self) -> List[Publisher]:
        return self.__publishers

    def add_review_to_game(self, game_id, review):
        game = self.get_game(game_id)
        if game:
            game.add_review(review)

def populate(repo: AbstractRepository):
    dir_name = os.path.dirname(os.path.abspath(__file__))
    games_file_name = os.path.join(dir_name, "data/games.csv")
    reader = GameFileCSVReader(games_file_name)
    reader.read_csv_file()
    games = reader.dataset_of_games
    genres = reader.dataset_of_genres
    publishers = reader.dataset_of_publishers

    # add games to the repo
    for game in games:
        repo.add_game(game)

    for genre in genres:
        repo.add_genre(genre)

    for publisher in publishers:
        repo.add_publisher(publisher)
