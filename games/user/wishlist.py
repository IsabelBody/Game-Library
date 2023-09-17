from games.domainmodel.model import Publisher, Genre, User, Game
from games.adapters.memory_repository import *
from games.user import services
from flask import Blueprint, request, session, redirect, flash, url_for

wishlist_blueprint = Blueprint('wishlist_bp', __name__)


@wishlist_blueprint.route('/wishlist', methods=['GET'])
def add_to_wishlist():
    game_id = request.args.get('game_id')
    # Retrieve game
    game = services.get_game(repo.repo_instance, int(game_id))
    current_user = session.get('user_name')
    # Add game to wishlist
    if game and current_user:
        services.add_wishlist_game(repo.repo_instance, current_user, game)
        flash(f'{game.title} has been added to your wishlist.', 'success')
    else:
        print("not game or user")
    return redirect(url_for('library_bp.library'))


@wishlist_blueprint.route('/remove_from_wishlist', methods=['GET'])
def remove_from_wishlist():
    game_id = request.args.get('game_id')
    # Retrieve game
    game = services.get_game(repo.repo_instance, int(game_id))
    current_user = session.get('user_name')
    # Add game to wishlist
    if game and current_user:
        services.remove_wishlist_game(repo.repo_instance, current_user, game)
        flash(f'{game.title} has been removed from your wishlist.', 'success')
    else:
        print("not game or user")

    return redirect(url_for('profile_bp.profile'))
