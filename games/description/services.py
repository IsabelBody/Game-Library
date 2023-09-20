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

    # Getting user
    user_name = session.get('user_name')
    user = services.get_user(repo, user_name)

    # Making a Review object.
    review = Review(user, game, rating, review_text)

    # Add the review to the game using the game's add_review method
    for reviewed in game.reviews:
        if isinstance(reviewed, Review):
            if reviewed.user == review.user:
                return "Game already reviewed"

    for rev in user.reviews:
        if isinstance(rev, Review) and review == rev:
            if rev.user == review.user:
                return "Game already reviewed"

    #user.add_review(review)
    #game.add_review(review)

    repo.add_review_to_game(game.game_id, review)
