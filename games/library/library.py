from flask import Blueprint, render_template

from games.library import services
from games.adapters.memory_repository import *
from games.adapters.repository import *



library_blueprint = Blueprint(
    'library_bp', __name__)


@library_blueprint.route('/library', methods=['GET'])
def library():
    num_games = services.get_number_of_games(repo.repo_instance)
    all_games = services.get_games(repo.repo_instance)
    return render_template(
        'gameLibrary.html',
        title = "Browse Games",
        heading='Browse Games',
        games=all_games,
        num_games=num_games)

