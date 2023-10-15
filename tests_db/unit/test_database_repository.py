import pytest

import games.adapters.repository as repo
from games.adapters.database_repository import SqlAlchemyRepository
from games.domainmodel.model import User, Game, Wishlist, Review, Publisher, Genre
from games.adapters.repository import RepositoryException

# User test cases

# Working


def test_repository_can_add_and_retrieve_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user1 = User("hasan", "password123")
    repo.add_user(user1)

    retrieved_user = repo.get_user("hasan")
    assert user1 == retrieved_user


def test_repository_does_not_retrieve_nonexistent_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = repo.get_user("Longfei")
    assert user is None


# # game test cases

def make_game(name=None, genre=None, id=None):
    if name is not None:
        game = Game(1, name)
    else:
        game = Game(3, "SaveerGame")
    game.price = 10.0
    game.release_date = "Oct 21, 2008"
    game.description = "A fun game"
    game.image_url = "saveer_image.jpg"
    game.website_url = "https://saveer-game.com"
    game.publisher_name = "saveerPublishing"
    if genre is not None:
        game.add_genre(genre)

    return game


def make_narnia_game(genre=None):

    game = Game(2, "Narnia")
    game.price = 10.0
    game.release_date = "Oct 21, 2008"
    game.description = "A magical adventure in the land of Narnia."
    game.image_url = "narnia_image.jpg"
    game.website_url = "https://narnia-game.com"
    if genre is not None:
        game.add_genre(genre)
    return game


def test_repository_can_add_game(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    new_game = make_game()

    old_len = len(repo.get_games())
    repo.add_game(new_game)
    new_len = len(repo.get_games())

    assert new_len == old_len + 1


def test_repository_can_retrieve_game(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    expected_game = repo.get_games()[7]
    # the id should return the same game
    matched_game = repo.get_game(expected_game.game_id)
    assert expected_game == matched_game


def test_repository_can_add_and_retrieve_games(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    game1 = make_game()
    game2 = make_narnia_game()
    original_games = repo.get_games()

    repo.add_game(game1)
    repo.add_game(game2)

    retrieved_games = repo.get_games()
    assert len(retrieved_games) == len(original_games) + 2
    assert game1 in retrieved_games
    assert game2 in retrieved_games


def test_repository_does_not_retrieve_nonexistent_game(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    game = repo.get_game(13434234231)
    assert game == None


def test_repository_can_retrieve_game_count(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    number_of_games = repo.get_number_of_games()
    actual_amount = len(repo.get_games())
    assert number_of_games == actual_amount


# # genre test cases

def test_repo_add_genre(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    new_genre = Genre("Dramedy")
    old_length = len(repo.get_genre())
    repo.add_genre(new_genre)

    assert len(repo.get_genre()) == (old_length + 1)


def test_repository_retrieves_games_by_genre(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    genre = Genre("Adventure")
    game1 = make_narnia_game(genre)
    game2 = make_game()
    game3 = make_game("hogwarts", genre)

    repo.add_game(game1)
    repo.add_game(game2)
    repo.add_game(game3)

    adventure_games = repo.get_games_for_genre("Adventure")
    assert len(adventure_games) == 397
    assert game1 in adventure_games
    assert game3 in adventure_games
    assert game2 not in adventure_games


def test_repository_doesnt_retrieve_invalid_genre(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    genre_name = "Advefsdfasdfasdfanture"

    games_in_genre = repo.get_games_for_genre(genre_name)
    assert isinstance(games_in_genre, list)
    assert len(games_in_genre) == 0


def test_repository_can_retrieve_unique_genres(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    num_unique_genres = repo.get_number_of_unique_genres()

    assert num_unique_genres == len(repo.get_genre())


def test_repo_retrieves_list_of_genres(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    genres = repo.get_genre()

    assert isinstance(genres, list)
    assert len(genres) > 0


# # Publisher test cases
def test_add_publisher(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    publisher = Publisher("saveerPublishing")
    original_publishers = repo.get_publishers()

    repo.add_publisher(publisher)
    retrieved_publishers = repo.get_publishers()

    assert len(original_publishers) + 1 == len(retrieved_publishers)


# # Reviews test cases

# WOkring
def test_repository_can_add_and_retrieve_reviews(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user = User("hasan", "Password123")
    game = make_narnia_game()
    repo.add_game(game)

    review = Review(user, game, 5, "I'm loving it")
    repo.add_review_to_game(2, review)

    retrieved_reviews = repo.get_reviews_for_game(2)
    assert len(retrieved_reviews) == 1
    assert retrieved_reviews[0] == review


def test_repository_can_remove_reviews(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = User("hasan", "Password123")
    game = make_game()
    review1 = Review(user, game, 5, "Im loving it")
    review2 = Review(user, game, 4, "I hate it")
    repo.add_user(user)
    repo.add_game(game)

    repo.add_review_to_game(game.game_id, review1)
    repo.add_review_to_game(game.game_id, review2)

    repo.remove_review(game.game_id, review1)

    retrieved_reviews = repo.get_reviews_for_game(game.game_id)
    assert len(retrieved_reviews) == 1
    assert review1 not in retrieved_reviews
    assert review2 in retrieved_reviews


def test_repository_does_not_remove_nonexistent_review(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = User("hasan", "Password123")
    game = make_game()
    review = Review(user, game, 5, "Im loving it")
    repo.add_user(user)
    repo.add_game(game)

    repo.remove_review(game.game_id, review)

    retrieved_reviews = repo.get_reviews_for_game(game.game_id)
    assert len(retrieved_reviews) == 1
    assert review in retrieved_reviews

# # Wishlist test cases


def test_repository_can_add_and_retrieve_wishlists(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = User("hasan", "Password123")
    game = make_game()
    repo.add_user(user)
    repo.add_game(game)
    repo.add_wishlist(user)
    repo.add_wishlist_game(user, game)
    retrieved_wishlist = repo.get_wishlist_games(user)
    assert retrieved_wishlist.size() == 1
    assert retrieved_wishlist[0] == game


def test_repository_can_remove_games_from_wishlist(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = User("hasan", "Password123")
    game1 = make_game()
    game2 = make_narnia_game()
    repo.add_user(user)
    repo.add_game(game1)
    repo.add_game(game2)
    repo.add_wishlist(user)

    repo.add_wishlist_game(user, game1)
    repo.add_wishlist_game(user, game2)

    repo.remove_wishlist_game(user, game1)

    retrieved_wishlist = repo.get_wishlist_games(user)
    assert retrieved_wishlist.size() == 1
    assert game1 not in retrieved_wishlist
    assert game2 in retrieved_wishlist


def test_repository_does_not_remove_nonexistent_game_from_wishlist(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = User("hasan", "Password123")
    game1 = make_game()
    repo.add_user(user)
    repo.add_game(game1)
    repo.add_wishlist(user)

    repo.remove_wishlist_game(user, game1)

    retrieved_wishlist = repo.get_wishlist_games(user)
    assert isinstance(retrieved_wishlist, Wishlist)
    assert retrieved_wishlist.size() == 0
