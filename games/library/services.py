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
    matching_games = []

    # checking each game


    matching_games = [game for game in games if query.lower() in game.title.lower()]
    return matching_games

def search_games(repo: AbstractRepository, query: str):
    games = repo.get_games()
    matching_games = []

    # making it so nothing is case sensitive
    query_lower = query.lower()

    # checking each game
    for game in games:
        # checking if any field matches the search
        if game not in matching_games: # making sure I don't add the same game twice.
            if (query_lower in game.title.lower() or
                query_lower in str(game.description).lower() or
                query_lower in game.publisher.publisher_name.lower() ):
                matching_games.append(game)
            # iterating through genres
            for genre in game.genres:
                if query_lower in str(genre).lower() and game not in matching_games:
                    matching_games.append(game)
    return matching_games

