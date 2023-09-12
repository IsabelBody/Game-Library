from games.adapters.repository import AbstractRepository


def get_game(repo: AbstractRepository, game_id):
    return repo.get_game(game_id)


def add_review(game_id, review_text, user_name, repo):
    # Check if the game exists (you might want to handle this case differently)
    game = repo.get_game(game_id)
    if not game:
        raise ValueError(f"Game with ID {game_id} not found.")

    # Create a Review object or dictionary with the review details (e.g., user_name, review_text)
    review = {
        'user_name': user_name,
        'review_text': review_text,
    }

    # Add the review to the game using the game's add_review method
    game.add_review(review)
