import pytest
import os

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from games import populate
from games.library.pagination import paginate
from games.library.services import get_games, search_games
from games.adapters.memory_repository import MemoryRepository
from games.domainmodel.model import Game, Genre
from games.library.services import *

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
        displayed_games, a, b, c = paginate(games, page_num) # only testing displayed games
        assert len(displayed_games) <= items_per_page  # checking less than 21 games per page


def test_search_games_empty_query(populated_repo):
    search_input = ""
    matching_games = search_games(populated_repo, search_input)

    assert len(matching_games) == 0  # non should be returned!


# the number of objects returned is correct
def test_get_number_of_games(populated_repo):
    game_amount = get_number_of_games(populated_repo)
    actual_amount = len(populated_repo.get_games())
    assert game_amount == actual_amount

# alternative search function using the service layer rather than directly interacting with our repository
def test_search_games_by_genre_service(populated_repo):
    result_games = search_games(populated_repo, "Action")
    assert len(result_games) > 0  # at least one game is in the genre!

    for game in result_games: # because a game has multiple genres sometimes
        assert Genre("Action") in game.genres  # matches?!