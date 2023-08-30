from games.adapters.repository import AbstractRepository


def get_game(repo: AbstractRepository, game_id):

    return repo.get_game(game_id)
