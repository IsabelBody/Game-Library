"""Initialize Flask app."""

from flask import Flask, render_template
import games.adapters.repository as repo
from games.adapters.memory_repository import populate
from games.adapters.memory_repository import MemoryRepository
from games.domainmodel.model import Game
from games.adapters.repository import AbstractRepository
from games.adapters.orm import metadata, map_model_to_tables
from flask import Flask
from pathlib import Path
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, clear_mappers, Session
from sqlalchemy.pool import NullPool
from games.adapters.repository import AbstractRepository
from games.adapters import memory_repository, database_repository, repository_populate
from games.adapters.orm import metadata, map_model_to_tables
from games.adapters.memory_repository import populate

def create_app(test_config=None):
    """Construct the core application."""

    # Create the Flask app object.
    app = Flask(__name__)
    database_uri = 'sqlite:///games.db'
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    app.config['SQLALCHEMY_ECHO'] = True
    # Configure the app from configuration-file settings.
    app.config.from_object('config.Config')
    data_path = Path('games') / 'adapters' / 'data'

    if test_config is not None:
        # Load test configuration, and override any configuration settings.
        app.config.from_mapping(test_config)
        data_path = app.config['TEST_DATA_PATH']

    # Here, configure your database settings.
    database_uri = app.config['SQLALCHEMY_DATABASE_URI']
    database_echo = app.config['SQLALCHEMY_ECHO']

    # Create the database engine.
    database_engine = create_engine(database_uri, connect_args={"check_same_thread": False}, poolclass=NullPool,
                                    echo=database_echo)
    metadata.create_all(database_engine)

    # Create the database session factory using sessionmaker (this has to be done once, in a global manner).
    session_factory = sessionmaker(autocommit=False, autoflush=True, bind=database_engine)

    # Initialize the DatabaseRepository instance with the session factory.
    repo.repo_instance = database_repository.SqlAlchemyRepository(session_factory)

    # Check if the database should be repopulated.
    # ...

    # this chunck does not work properly
    if len(database_engine.table_names()) == 0:
        print("REPOPULATING DATABASE...")
        # For testing or first-time use of the web application, reinitialize the database.
        clear_mappers()
        # Conditionally create database tables.
        # Remove any data from the tables.
        for table in reversed(metadata.sorted_tables):
            with database_engine.connect() as conn:
                conn.execute(table.delete())

        # Generate mappings that map domain model classes to the database tables.
        map_model_to_tables()

        repository_populate.populate(data_path, repo.repo_instance)
        print("REPOPULATING DATABASE... FINISHED")
    else:
        map_model_to_tables()

    # ...

    # Register blueprints.
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

        from .user import profile
        app.register_blueprint(profile.profile_blueprint)

        from .user import wishlist
        app.register_blueprint(wishlist.wishlist_blueprint)

    # Request and teardown handlers for managing database sessions.
    @app.before_request
    def before_flask_http_request_function():
        if isinstance(repo.repo_instance, database_repository.SqlAlchemyRepository):
            repo.repo_instance.reset_session()

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        if isinstance(repo.repo_instance, database_repository.SqlAlchemyRepository):
            repo.repo_instance.close_session()

    return app
