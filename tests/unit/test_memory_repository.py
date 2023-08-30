import pytest
from games.adapters.memory_repository import MemoryRepository, populate
from games.domainmodel.model import Genre, Game
from games.library.services import get_games, search_games
import sys
import os


@pytest.fixture
def in_memory_repo():
    # Create and populate the repository
    repo = MemoryRepository()
    populate(repo)
    return repo


def test_repository_gets_number_of_unique_genres(in_memory_repo):
    num_unique_genres = in_memory_repo.get_number_of_unique_genres()

    assert num_unique_genres == len(in_memory_repo.get_genre())


def test_repository_adds_by_one_for_genres(in_memory_repo):
    new_genre = Genre("Dramedy")
    old_length = len(in_memory_repo.get_genre())
    in_memory_repo.add_genre(new_genre)

    assert len(in_memory_repo.get_genre()) == (old_length + 1)


def test_repository_adds_game_object(in_memory_repo):
    new_game = Game(256, "Narnia")
    old_len = len(in_memory_repo.get_games())
    in_memory_repo.add_game(new_game)
    new_len = len(in_memory_repo.get_games())

    assert new_len == old_len + 1


def test_repository_games_only_for_certain_genre(in_memory_repo):
    genre_name = "Adventure"

    games_in_genre = in_memory_repo.get_games_for_genre(genre_name) # all games in that genre
    for game in in_memory_repo.get_games(): # every game in the system
        if game not in games_in_genre: # if the game aint in the list, its not in that genre
            assert all(genre.genre_name != genre_name for genre in game.genres) # therefore, every genre for that game is not adventure

    for game in games_in_genre: # if game is in list
        assert any(genre.genre_name == genre_name for genre in game.genres) # at least one of its genres is the right genre.


# Testing the search for the input box.
def test_search_games_by_title(in_memory_repo):
    search_input = "100 Seconds" # title name must come up
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
    search_input = "qcf design"
    results = search_games(in_memory_repo, search_input)

    assert len(results) > 0  # at least the publisher's games should appear

    for game in results:
        title_lower = game.title.lower()
        publisher_lower = game.publisher.publisher_name.lower()
        search_input_lower = search_input.lower()

        assert search_input_lower in title_lower or \
               search_input_lower in publisher_lower or \
               any(search_input in str(genre).lower() for genre in game.genres)

# we can recieve a specific game
def test_retrieve_game_by_id(in_memory_repo):
    expected_game = in_memory_repo.get_games()[7]
    # the id should return the same game
    matched_game = in_memory_repo.get_game(expected_game.game_id)
    assert expected_game == matched_game