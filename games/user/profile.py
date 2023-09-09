from flask import Blueprint, request, render_template

profile_blueprint = Blueprint('profile_bp', __name__)

@profile_blueprint.route('/profile', methods=['GET'])
def profile():
    return render_template(
        'profile.html',
        title="Profile",
        heading='My Profile',
        )