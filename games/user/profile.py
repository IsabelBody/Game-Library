from flask import Blueprint, request, render_template, session
from games.adapters.memory_repository import *
from games.user import wishlist, services
from games.user.reviews import get_user_reviews

profile_blueprint = Blueprint('profile_bp', __name__)


@profile_blueprint.route('/profile', methods=['GET'])
def profile():
    user_name = session.get('user_name')
    current_user = services.get_user(repo.repo_instance, user_name)
    wishlist_games = services.get_wishlist_games(
        repo.repo_instance, current_user)
    reviews = get_user_reviews()
    return render_template(
        'profile.html',
        title="Profile",
        heading='My Profile',
        wishlist_games=wishlist_games,
        reviews = reviews
    )
