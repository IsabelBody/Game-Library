"""Initialize Flask app."""

from flask import Flask, render_template
import games.adapters.repository as repo
from games.adapters.memory_repository import populate
from games.adapters.memory_repository import MemoryRepository
from games.domainmodel.model import Game




def create_app():
    """Construct the core application."""

    # Create the Flask app object.
    app = Flask(__name__)
    app.debug = True
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

    repo.repo_instance = MemoryRepository()
    populate(repo.repo_instance)



    return app
