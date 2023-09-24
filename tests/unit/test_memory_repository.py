import pytest
from games.adapters.memory_repository import MemoryRepository, populate
from games.domainmodel.model import Genre, Game, Publisher, User, Review
from games.library.services import get_games, search_games
import sys
import os


@pytest.fixture
def in_memory_repo():
    # Create and populate the repository
    repo = MemoryRepository()
    populate(repo)
    return repo


# Test the number of unique genres in the dataset
def test_repository_gets_number_of_unique_genres(in_memory_repo):
    num_unique_genres = in_memory_repo.get_number_of_unique_genres()

    assert num_unique_genres == len(in_memory_repo.get_genre())


# Test repository adds a new genre, and the count of genres increases by 1


def test_repository_adds_by_one_for_genres(in_memory_repo):
    new_genre = Genre("Dramedy")
    old_length = len(in_memory_repo.get_genre())
    in_memory_repo.add_genre(new_genre)

    assert len(in_memory_repo.get_genre()) == (old_length + 1)


# Test repository can add a game object


def test_repository_adds_game_object(in_memory_repo):
    new_game = Game(256, "Narnia")
    old_len = len(in_memory_repo.get_games())
    in_memory_repo.add_game(new_game)
    new_len = len(in_memory_repo.get_games())

    assert new_len == old_len + 1


# Test repository retrieves correct number of game objects


def test_repository_retrieves_correct_number_of_games(in_memory_repo):
    game_amount = in_memory_repo.get_number_of_games()
    actual_amount = len(in_memory_repo.get_games())
    assert game_amount == actual_amount


def test_repository_games_only_for_certain_genre(in_memory_repo):
    genre_name = "Adventure"

    games_in_genre = in_memory_repo.get_games_for_genre(
        genre_name)  # all games in that genre
    for game in in_memory_repo.get_games():  # every game in the system
        if game not in games_in_genre:  # if the game aint in the list, its not in that genre
            # therefore, every genre for that game is not adventure
            assert all(genre.genre_name != genre_name for genre in game.genres)

    for game in games_in_genre:  # if game is in list
        # at least one of its genres is the right genre.
        assert any(genre.genre_name == genre_name for genre in game.genres)


# Testing the search for the input box.
def test_search_games_by_title(in_memory_repo):
    search_input = "100 Seconds"  # title name must come up
    results = search_games(in_memory_repo, search_input)

    assert len(results) > 0  # the titled game should appear

    for game in results:
        title_lower = game.title.lower()
        publisher_lower = game.publisher.publisher_name.lower()
        search_input_lower = search_input.lower()

        assert search_input_lower in title_lower or \
               search_input_lower in publisher_lower or \
               any(search_input in str(genre).lower() for genre in game.genres)


def test_search_games_publisher(in_memory_repo):
    search_input = "Activision"
    results = search_games(in_memory_repo, search_input)

    assert len(results) > 0  # at least the publisher's games should appear

    for game in results:
        title_lower = game.title.lower()
        publisher_lower = game.publisher.publisher_name.lower()
        search_input_lower = search_input.lower()

        assert search_input_lower in title_lower or \
               search_input_lower in publisher_lower or \
               any(search_input in str(genre).lower() for genre in game.genres)

    result_games = search_games(in_memory_repo, '', None, search_input)
    assert len(result_games) > 0
    for game in result_games:
        assert Publisher("Activision") == game.publisher


# Test repository can retrieve a game object


def test_retrieve_game_by_id(in_memory_repo):
    expected_game = in_memory_repo.get_games()[7]
    # the id should return the same game
    matched_game = in_memory_repo.get_game(expected_game.game_id)
    assert expected_game == matched_game


# Testing add review to game in memory_repository
def test_memory_repo_add_review_to_game(in_memory_repo):
    game_id = 13
    title = "Zombies"
    game = Game(game_id, title)
    user = User("natalie", "Nate1234")
    comment = "This game was horrible"
    rating = 1
    review = Review(user, game, rating, comment)
    in_memory_repo.add_game(game)
    in_memory_repo.add_review_to_game(game_id, review)

    game_return = in_memory_repo.get_game(13)

    assert review in game_return.reviews


# Test doesn't add different reviews for same game by same user
def test_memory_repo_doesnt_add_duplicate_reviews(in_memory_repo):
    game_id = 13
    title = "Zombies"
    game = Game(game_id, title)
    user = User("natalie", "Nate1234")
    comment = "This game was horrible"
    rating = 1
    review = Review(user, game, rating, comment)

    comment2 = "Awesome game!"
    rating2 = 5
    review2 = Review(user, game, rating2, comment2)

    in_memory_repo.add_game(game)
    in_memory_repo.add_review_to_game(game_id, review)
    in_memory_repo.add_review_to_game(game_id, review2)
    game_return = in_memory_repo.get_game(13)

    assert len(game_return.reviews) == 1





