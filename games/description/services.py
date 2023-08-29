from games.adapters.repository import AbstractRepository


def get_number_of_games(repo: AbstractRepository):
    return repo.get_number_of_games()


def get_games(repo: AbstractRepository):
    games = repo.get_games()
    game_dicts = []
    for game in games:
        print(game)
        game_dict = {'game_id': game.game_id,
                     'title': game.title,
                     'game_url': game.release_date,
                     "description": game.description,
                     "image_url": game.image_url}
        game_dicts.append(game_dict)
    return game_dicts


def get_genres(repo: AbstractRepository):
    genres = repo.get_genre()
    genres_names = [genre for genre in genres]

    return genres_names


def get_games_for_genre(repo: AbstractRepository, genre_name):
    # Implement this method in your repository.
    games = repo.get_games_for_genre(genre_name)
    game_dicts = [{'game_id': game.game_id, 'title': game.title}
                  for game in games]
    return game_dicts
