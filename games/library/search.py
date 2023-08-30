from flask import Blueprint, request, render_template
from games.adapters.memory_repository import *
from games.library import services
from games.library.pagination import paginate

search_blueprint = Blueprint('search_bp', __name__)


@search_blueprint.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '').strip()
    page = int(request.args.get('page', 1))
    genre = request.args.get('genre')
    publisher = request.args.get('publisher')

    if not publisher:
        publisher = None
    if not genre:
        genre = None

    try:
        if query:
            matching_games = services.search_games(
                repo.repo_instance, query, genre, publisher)
            displayed_games, total_pages, _, _ = paginate(matching_games, page)
            num_results = len(matching_games)
        else:
            num_results = 0
            displayed_games = []
            total_pages = 0
    except ValueError as e:
        # Handle the "no results found" scenario
        num_results = 0
        displayed_games = []
        total_pages = 0

    return render_template(
        'searchResults.html',
        query=query,
        matching_games=displayed_games,
        num_results=num_results,
        total_pages=total_pages,
        current_page=page
    )
