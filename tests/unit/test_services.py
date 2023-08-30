from games.library.services import *
from games.library.search import *
from games.domainmodel.model import Game, Genre
from games.adapters.memory_repository import MemoryRepository
from games.library.services import get_games, search_games
from games.library.pagination import paginate
from games.description.services import *
from games import populate

import pytest
import os

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture
def populated_repo():
    repo = MemoryRepository()
    populate(repo)
    return repo


# testing the pagination function, it should produce 21 per page.
def test_pagination_populated_repo(populated_repo):
    games = get_games(populated_repo)
    assert len(games) > 0  # the repo isn't empty.
    items_per_page = 21
    total_pages = (len(games) + items_per_page - 1) // items_per_page

    for page_num in range(1, total_pages + 1):
        displayed_games, a, b, c = paginate(
            games, page_num)  # only testing displayed games
        # checking less than 21 games per page
        assert len(displayed_games) <= items_per_page

# Test inserting empty search key throws exception


def test_search_games_empty_query(populated_repo):
    with pytest.raises(ValueError):
        search_games(populated_repo, "")


# the number of objects returned is correct
def test_get_number_of_games(populated_repo):
    game_amount = get_number_of_games(populated_repo)
    actual_amount = len(populated_repo.get_games())
    assert game_amount == actual_amount

# alternative search function using the service layer rather than directly interacting with our repository

# Test getting games for a search key 'genre'


def test_search_games_by_genre_service(populated_repo):
    result_games = search_games(populated_repo, "Action")
    assert len(result_games) > 0  # at least one game is in the genre!

    games = search_games(populated_repo, 'action')
    assert len(games) == 485

# Test service layer return an existing game object


def test_returns_existing_game(populated_repo):
    # get game
    game = get_game(populated_repo, 3010)

    print(game)
    # get game title -> equal Xpand Rally
    assert game['title'] == 'Xpand Rally'

# Test getting games for a search key 'publisher


def test_get_games_by_publisher_search_key(populated_repo):
    games = search_games(populated_repo, '8floor')
    print(games)
    assert len(games) == 5

# Test inserting non-existing search key throws exception


def test_inserting_non_existing_search_key(populated_repo):
    with pytest.raises(ValueError):
        search_games(populated_repo, "fdasfadsfsafdafdasfadfdasad")


# def test_get_game_with_search_key(populated_repo):
#     games = search_games('Xpand')
#     # check game is of type Game
#     assert isinstance(game, Game)
#     print(game)
#     # get game title -> equal Xpand Rally
#     assert game['title'] == 'Xpand Rally'
