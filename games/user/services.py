from games.adapters.repository import AbstractRepository
from games.domainmodel.model import Game, User
from typing import List


def get_game(repo: AbstractRepository, game_id):
    return repo.get_game(game_id)


def add_wishlist_game(repo: AbstractRepository, user_name, game: Game):
    user = repo.get_user(user_name)
    repo.add_wishlist_game(user, game)


def add_wishlist(repo: AbstractRepository, user_name):
    user = repo.get_user(user_name)
    repo.add_wishlist(user)


def get_wishlist_games(repo: AbstractRepository, user) -> List[Game]:
    return repo.get_wishlist_games(user)


def get_user(repo: AbstractRepository, user_name: str):
    user = repo.get_user(user_name)
    if user is None:
        return None
    return user


def remove_wishlist_game(repo: AbstractRepository, user_name, game: Game):
    user = repo.get_user(user_name)
    repo.remove_wishlist_game(user, game)
