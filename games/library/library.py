from flask import Blueprint, request, url_for
from games.adapters.memory_repository import *
from games.library import services
from games.library.pagination import paginate

library_blueprint = Blueprint(
    'library_bp', __name__)


@library_blueprint.route('/library', methods=['GET'])
def library():
    page = int(request.args.get('page', 1))
    num_games = services.get_number_of_games(repo.repo_instance)
    all_games = services.get_games(repo.repo_instance)

    displayed_games, total_pages, start_idx, end_idx = paginate(all_games, page)

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
    genre_name = request.args.get('genre')
    page = int(request.args.get('page', 1))

    # Retrieve games for the specified genre using the services module.
    games = services.get_games_for_genre(repo.repo_instance, genre_name)
    games.sort(key=lambda game: game['title']) # sorting the output alphabetically

    displayed_games, total_pages, start_idx, end_idx = paginate(games, page)

    # Calculate URLs for pagination
    prev_page_url = None
    next_page_url = None

    if page > 1:
        prev_page_url = url_for('library_bp.games_by_genre', genre=genre_name, page=page - 1)

    if page < total_pages:
        next_page_url = url_for('library_bp.games_by_genre', genre=genre_name, page=page + 1)

    return render_template(
        'byGenre.html',
        title='Games',
        games_title=f'Games in the {genre_name} genre',
        games= displayed_games,
        prev_page_url=prev_page_url,
        next_page_url=next_page_url,
        current_page=page,
        total_pages=total_pages
    )


