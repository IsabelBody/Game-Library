from games.adapters.repository import AbstractRepository


def get_number_of_games(repo: AbstractRepository):
    return repo.get_number_of_games()


def get_games(repo: AbstractRepository):
    games = repo.get_games()

    games = sorted(games, key=lambda game: game.title) # sorting based on alphabetical order.
    game_dicts = []
    for game in games:
        game_dict = {'game_id': game.game_id,
                     'title': game.title,
                     'game_url': game.release_date}
        game_dicts.append(game_dict)
    return game_dicts


def get_genres(repo: AbstractRepository):
    genres = repo.get_genre()
    genres_names = [genre for genre in genres]

    return genres_names


def get_games_for_genre(repo: AbstractRepository, genre_name):
    games = repo.get_games_for_genre(genre_name)  # Implement this method in your repository.
    game_dicts = [{'game_id': game.game_id, 'title': game.title} for game in games]
    return game_dicts


# search bar stuff
def search_games(repo: AbstractRepository, query: str):
    games = repo.get_games()
    matching_games = [game for game in games if query.lower() in game.title.lower()]
    return matching_games