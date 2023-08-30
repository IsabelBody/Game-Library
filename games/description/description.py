from flask import Blueprint, request, render_template

from games.adapters.memory_repository import *
from games.description import services

description_blueprint = Blueprint(
    'description_bp', __name__)


@description_blueprint.route('/description', methods=['GET'])
def description():
    game_id = int(request.args.get('game_id'))
    game = services.get_game(repo.repo_instance, game_id)
    return render_template('gameDescription.html', game=game)
