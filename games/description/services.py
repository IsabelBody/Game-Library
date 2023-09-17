from games.adapters.repository import AbstractRepository
from games.domainmodel.model import Review
from games.user import services
from flask import Blueprint, request, render_template, session


def get_game(repo: AbstractRepository, game_id):
    return repo.get_game(game_id)


def add_review(game_id, review_text, user_name, repo, rating):
    # Check if the game exists (you might want to handle this case differently)
    game = repo.get_game(game_id)
    if not game:
        raise ValueError(f"Game with ID {game_id} not found.")

    # getting user
    user_name = session.get('user_name')
    user = services.get_user(repo, user_name)


    # making a Review object.
    review = Review(user, game, rating, review_text)

    # Add the review to the game using the game's add_review method
    game.add_review(review)
    user.add_review(review)
