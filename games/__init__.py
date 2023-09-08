"""Initialize Flask app."""

from flask import Flask, render_template
import games.adapters.repository as repo
from games.adapters.memory_repository import populate
from games.adapters.memory_repository import MemoryRepository
from games.domainmodel.model import Game
from games.adapters.repository import AbstractRepository
from pathlib import Path


def create_app(test_config=None):
    """Construct the core application."""

    # Create the Flask app object.
    app = Flask(__name__)
    app.debug = True

    # Configure the app from configuration-file settings.
    app.config.from_object('config.Config')
    data_path = Path('games') / 'adapters' / 'data'

    if test_config is not None:
        # Load test configuration, and override any configuration settings.
        app.config.from_mapping(test_config)
        data_path = app.config['TEST_DATA_PATH']

    # creates the ability to redirect to the homepage.
    with app.app_context():
        from .home import home
        app.register_blueprint(home.home_blueprint)

        from .library import library
        app.register_blueprint(library.library_blueprint)

        from .description import description
        app.register_blueprint(description.description_blueprint)

        from .library import search
        app.register_blueprint(search.search_blueprint)

        from .authentication import authentication
        app.register_blueprint(authentication.authentication_blueprint)

    repo.repo_instance = MemoryRepository()
    populate(repo.repo_instance)

    def getGenres(repo: AbstractRepository):
        genres = repo.get_genre()
        genre_options = [current_genre.genre_name for current_genre in genres]
        return genre_options

    def getPublishers(repo: AbstractRepository):
        publishers = repo.get_publishers()
        publisher_options = [
            current_publisher.publisher_name for current_publisher in publishers]
        return publisher_options

    @app.context_processor
    def inject_genre_options():
        genre_options = getGenres(repo.repo_instance)
        publisher_options = getPublishers(repo.repo_instance)
        return dict(genre_options=genre_options, publisher_options=publisher_options)

    return app
