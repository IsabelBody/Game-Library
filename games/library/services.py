from games.adapters.repository import AbstractRepository


def get_number_of_games(repo: AbstractRepository):
    return repo.get_number_of_games()


def get_games(repo: AbstractRepository):
    games = repo.get_games()

    # sorting based on alphabetical order.
    games = sorted(games, key=lambda game: game.title)
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
    # Implement this method in your repository.
    games = repo.get_games_for_genre(genre_name)
    game_dicts = [{'game_id': game.game_id, 'title': game.title}
                  for game in games]
    return game_dicts


# search bar stuff
def search_games(repo: AbstractRepository, query: str, genre_query: str = None, publisher: str = None):
    games = repo.get_games()
    matching_games = []

    # making it so nothing is case sensitive
    query_lower = query.lower()

    # checking each game
    for game in games:
        genre_names = [genre.genre_name for genre in game.genres]
        # checking if any field matches the search
        if game not in matching_games:  # making sure I don't add the same game twice.
            if (query_lower in game.title.lower() or
                query_lower in str(game.description).lower() or
                query_lower in game.publisher.publisher_name.lower() or
                    any(query_lower in name.lower() for name in genre_names)):

                if ((publisher is None or publisher in game.publisher.publisher_name) and (genre_query is None or any(genre_query.lower() in name.lower() for name in genre_names))):
                    matching_games.append(game)
    if len(matching_games) == 0:
        raise ValueError("No results found for the search query.")
    return matching_games
