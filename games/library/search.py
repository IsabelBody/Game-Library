from flask import Blueprint, request, url_for

from games.adapters.memory_repository import *
from games.library import services
from games.library.pagination import paginate

search_blueprint = Blueprint(
    'search_bp', __name__)

# Search button resulting html page


@search_blueprint.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '').strip()
    page = int(request.args.get('page', 1))  # Get page number from the search
    genre = request.args.get('genre')
    publisher = request.args.get('publisher')
    # Check if publisher parameter is not provided
    if not publisher:
        publisher = None
    if not genre:
        genre = None
    try:
        matching_games = services.search_games(
            repo.repo_instance, query, genre, publisher)
        num_results = len(matching_games)

        displayed_games, total_pages, start_idx, end_idx = paginate(
            matching_games, page)

    except ValueError as e:
        # when there are 0 results.
        num_results = 0
        displayed_games = []
        total_pages = 0

    return render_template(
        'searchResults.html',
        query=query,
        matching_games=displayed_games,
        num_results=num_results,
        total_pages=total_pages,
        current_page=page)
