from flask import Blueprint, request, url_for

from games.adapters.memory_repository import *
from games.library import services

library_blueprint = Blueprint(
    'library_bp', __name__)


@library_blueprint.route('/library', methods=['GET'])
def library():
    page = int(request.args.get('page', 1))
    num_games = services.get_number_of_games(repo.repo_instance)
    all_games = services.get_games(repo.repo_instance)
    games_per_page = 21

    # pagination stuff
    total_pages = (num_games + games_per_page - 1) // games_per_page  # Calculate total number of pages
    start_idx = (page - 1) * games_per_page
    end_idx = start_idx + games_per_page
    displayed_games = all_games[start_idx:end_idx]

    all_genres = services.get_genres(repo.repo_instance)
    return render_template(
        'gameLibrary.html',
        title="Browse Games",
        heading='Browse Games',
        games=displayed_games,
        num_games=num_games,
        total_pages=total_pages,
        current_page=page,
        given_genres=all_genres)

# better if we leave it as library and specify genre, use if statement to see if there is a genre 
@library_blueprint.route('/games_by_genre', methods=['GET'])
def games_by_genre():
    games_per_page = 3
    given_genres = services.get_genres(repo.repo_instance)
    # Read query parameters.
    genre_name = request.args.get('genre')
    cursor = request.args.get('cursor')

    if cursor is None:
        # No cursor query parameter, so initialize cursor to start at the beginning.
        cursor = 0
    else:
        # Convert cursor from string to int.
        cursor = int(cursor)

    # Retrieve games for the specified genre using the services module.
    games = services.get_games_for_genre(repo.repo_instance, genre_name)
    # will the above line throw an error if genre_name is empty

    first_game_url = None
    last_game_url = None
    next_game_url = None
    prev_game_url = None

    if cursor > 0:
        # There are preceding games, so generate URLs for the 'previous' and 'first' navigation buttons.
        prev_game_url = url_for('library_bp.games_by_genre', genre=genre_name, cursor=cursor - games_per_page)
        first_game_url = url_for('library_bp.games_by_genre', genre=genre_name)

    if cursor + games_per_page < len(games):
        # There are further games, so generate URLs for the 'next' and 'last' navigation buttons.
        next_game_url = url_for('library_bp.games_by_genre', genre=genre_name, cursor=cursor + games_per_page)

        last_cursor = games_per_page * (len(games) // games_per_page)
        if len(games) % games_per_page == 0:
            last_cursor -= games_per_page
        last_game_url = url_for('library_bp.games_by_genre', genre=genre_name, cursor=last_cursor)

    # Generate the webpage to display the games.
    return render_template(
        'byGenre.html',
        given_genres=given_genres,
        title='Games',
        games_title='Games in the ' + genre_name + ' genre',
        games=games,
        first_game_url=first_game_url,
        last_game_url=last_game_url,
        prev_game_url=prev_game_url,
        next_game_url=next_game_url
    )
