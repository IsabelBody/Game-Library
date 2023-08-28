import pytest
from games.adapters.memory_repository import MemoryRepository, populate
from games.domainmodel.model import Genre, Game


@pytest.fixture
def in_memory_repo():
    # Create and populate the repository
    repo = MemoryRepository()
    populate(repo)
    return repo


def test_repository_gets_number_of_unique_genres(in_memory_repo):
    num_unique_genres = in_memory_repo.get_number_of_unique_genres()

    # Add your assertion here
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


# isabel - could you help me check this please?
def test_repository_games_only_for_certain_genre(in_memory_repo):
    genre_name = "Adventure"

    games_in_genre = in_memory_repo.get_games_for_genre(genre_name)
    for game in in_memory_repo.get_games():
        if game not in games_in_genre:
            assert all(genre.genre_name != genre_name for genre in game.genres)

    for game in games_in_genre:
        assert any(genre.genre_name == genre_name for genre in game.genres)
