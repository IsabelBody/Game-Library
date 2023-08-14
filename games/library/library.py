from flask import Blueprint, render_template

library_blueprint = Blueprint(
    'library_bp', __name__)


@library_blueprint.route('/library', methods=['GET'])
def library():
    return render_template('gameLibrary.html')
