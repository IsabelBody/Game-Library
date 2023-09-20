from games.library.services import *
from games.library.search import *
from games.domainmodel.model import Game, Genre
from games.adapters.memory_repository import MemoryRepository
from games.library.services import get_games, search_games
from games.library.pagination import paginate
from games.description.services import get_game, add_review
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


# LIBRARY.PAGINATION
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


# LIBRARY.SERVICES
# Test inserting empty search key throws exception


def test_search_games_empty_query(populated_repo):
    with pytest.raises(ValueError):
        search_games(populated_repo, "")


# Test inserting non-existing search key throws exception


def test_inserting_non_existing_search_key(populated_repo):
    with pytest.raises(ValueError):
        search_games(populated_repo, "fdasfadsfsafdafdasfadfdasad")


# Test the number of objects returned is correct


def test_get_number_of_games(populated_repo):
    game_amount = get_number_of_games(populated_repo)
    actual_amount = len(populated_repo.get_games())
    assert game_amount == actual_amount


# alternative search function using the service layer rather than directly interacting with our repository
# Test getting games for a search key ‘genre’


def test_search_games_by_genre(populated_repo):
    result_games = search_games(populated_repo, "", "Action")
    assert len(result_games) > 0  # at least one game is in the genre!
    for game in result_games:
        # The genre must exist in the game
        assert Genre("Action") in game.genres


# Test getting games for a search key 'publisher'


def test_get_games_by_publisher_search_key(populated_repo):
    result_games = search_games(populated_repo, '', None, 'Activision')
    assert len(result_games) > 0
    for game in result_games:
        assert Publisher("Activision") == game.publisher


# Test find specific game with search key


def test_get_game_with_search_key(populated_repo):
    game = search_games(populated_repo, 'Xpand Rally')[0]
    # check game is of type Game
    assert isinstance(game, Game)

    # get game title -> equal Xpand Rally
    assert game.title == 'Xpand Rally'


# DESCRIPTION.SERVICES
# Test service layer return an existing game object


def test_returns_existing_game(populated_repo):
    # get game
    game = get_game(populated_repo, 3010)
    assert isinstance(game, Game)
    # get game title -> equal Xpand Rally
    assert game.title == 'Xpand Rally'

    expected_game = get_games(populated_repo)[7]
    # the id should return the same game
    matched_game = get_game(populated_repo, expected_game['game_id'])
    assert expected_game['title'] == matched_game.title
