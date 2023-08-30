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
    games = repo.get_games_for_genre(genre_name)
    game_dicts = [{'game_id': game.game_id, 'title': game.title}
                  for game in games]
    return game_dicts


# search bar stuff
def search_games(repo: AbstractRepository, query: str, genre_query: str = None, publisher_query: str = None):
    # making it so nothing is case sensitive
    query_lower = query.lower()

    def matches_query(game):
        return (query_lower in game.title.lower() or
                query_lower in str(game.description).lower() or
                query_lower in game.publisher.publisher_name.lower())

    def matches_genre(game):
        if genre_query is None:
            return True  # No genre_query provided, so all genres match
        genre_names = [genre.genre_name for genre in game.genres]
        return any(query_lower in name.lower() for name in genre_names)

    def matches_publisher(game):
        return publisher_query is None or publisher_query in game.publisher.publisher_name

    games = repo.get_games()
    matching_games = [game for game in games if matches_query(game)
                      and matches_genre(game) and matches_publisher(game)]

    if not matching_games:
        raise ValueError("No results found for the search query.")

    return matching_games
