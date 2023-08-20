from flask import Blueprint, request, render_template

from games.adapters.memory_repository import *
from games.library import services

description_blueprint = Blueprint(
    'description_bp', __name__)

@description_blueprint.route('/description', methods=['GET'])
def description():
    game_id= int(request.args.get('game_id'))
    all_games = services.get_games(repo.repo_instance)

    found_game = None
    for game in all_games:
        if game['game_id'] == game_id:
            found_game = game
            break
    if found_game:
        print("Found:", found_game['title'])
    else:
        print("Object not found")


    return render_template('gameDescription.html', game=found_game)
