from flask import Blueprint, render_template

home_blueprint = Blueprint(
    'home_bp', __name__)


# leaving this as a slash so that it is the default page on open.
@home_blueprint.route('/', methods=['GET'])
def home():
    return render_template('home.html')
