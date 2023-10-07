from games.authentication.authentication import login_required
from games.domainmodel.model import Publisher, Genre, User, Game
import games.adapters.repository as repo
from games.user import services
from flask import Blueprint, request, session, redirect, flash, url_for

wishlist_blueprint = Blueprint('wishlist_bp', __name__)


@wishlist_blueprint.route('/wishlist', methods=['GET'])
@login_required
def add_to_wishlist():

    # game retrieval not working
    game_id = request.args.get('game_id')
    game = services.get_game(repo.repo_instance, int(game_id))


    username = session.get('user_name')

    user = repo.repo_instance.get_user(username)

    # Add game to wishlist
    if game and username:
        services.add_wishlist_game(repo.repo_instance, username, game)
        flash(f'{game.title} has been added to your wishlist.', 'success')
    else:
        print("not game or user")
        return redirect(url_for('authentication_bp.register'))

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
