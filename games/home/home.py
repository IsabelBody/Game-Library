from flask import Blueprint, render_template
from games.adapters.repository import AbstractRepository

from games.adapters.memory_repository import *
from games.library import services


home_blueprint = Blueprint(
    'home_bp', __name__)


# leaving this as a slash so that it is the default page on open.
@home_blueprint.route('/', methods=['GET'])
def home():
    return render_template('home.html')
