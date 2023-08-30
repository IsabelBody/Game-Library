from games.adapters.repository import AbstractRepository


def get_game(repo: AbstractRepository, game_id):
    raw_game = repo.get_game(game_id)
    genre_names = ', '.join([genre.genre_name for genre in raw_game.genres])

    game = {'game_id': raw_game.game_id,
            'title': raw_game.title,
            'release_date': raw_game.release_date,
            "description": raw_game.description,
            "image_url": raw_game.image_url,
            "reviews": raw_game.reviews,
            "publisher": raw_game.publisher.publisher_name,
            "genres": genre_names,
            "price": raw_game.price}
    return game
