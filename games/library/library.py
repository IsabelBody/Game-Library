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
    games_per_page = 21  # Adjust this as needed
    given_genres = services.get_genres(repo.repo_instance)
    genre_name = request.args.get('genre')
    page = int(request.args.get('page', 1))  # Use 'page' instead of 'cursor'

    # Retrieve games for the specified genre using the services module.
    games = services.get_games_for_genre(repo.repo_instance, genre_name)
    games.sort(key=lambda game: game['title'])

    # Calculate total pages for pagination
    total_pages = (len(games) + games_per_page - 1) // games_per_page

    # Calculate the start and end indices for the games on the current page
    start_idx = (page - 1) * games_per_page
    end_idx = start_idx + games_per_page
    displayed_games = games[start_idx:end_idx]

    # Calculate URLs for pagination
    prev_page_url = None
    next_page_url = None

    if page > 1:
        prev_page_url = url_for('library_bp.games_by_genre', genre=genre_name, page=page - 1)

    if page < total_pages:
        next_page_url = url_for('library_bp.games_by_genre', genre=genre_name, page=page + 1)

    return render_template(
        'byGenre.html',
        given_genres=given_genres,
        title='Games',
        games_title=f'Games in the {genre_name} genre',
        games= displayed_games,
        prev_page_url=prev_page_url,
        next_page_url=next_page_url,
        current_page=page,
        total_pages=total_pages
    )



# Search button resulting html page. Is this the best place for it?
@library_blueprint.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '').strip()
    page = int(request.args.get('page', 1))  # Get page number from query parameter
    games_per_page = 21

    if query:
        matching_games = services.search_games(repo.repo_instance, query)
        num_results = len(matching_games)

        start_idx = (page - 1) * games_per_page
        end_idx = start_idx + games_per_page
        displayed_games = matching_games[start_idx:end_idx]
    else:
        matching_games = []
        num_results = 0
        displayed_games = []

    total_pages = (num_results + games_per_page - 1) // games_per_page

    return render_template(
        'searchResults.html',
        query=query,
        matching_games=displayed_games,
        num_results=num_results,
        total_pages=total_pages,
        current_page=page)
