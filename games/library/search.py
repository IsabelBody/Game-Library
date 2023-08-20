from flask import Blueprint, request, url_for

from games.adapters.memory_repository import *
from games.library import services

search_blueprint = Blueprint(
    'search_bp', __name__)

# Search button resulting html page
@search_blueprint.route('/search', methods=['GET'])
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
