from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from games.adapters.memory_repository import *
from games.authentication.authentication import login_required
from games.description import services
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, IntegerRangeField
from wtforms.validators import DataRequired, NumberRange

description_blueprint = Blueprint(
    'description_bp', __name__)

class ReviewForm(FlaskForm):
    review_text = TextAreaField('Write your review', validators=[DataRequired()])
    rating = IntegerRangeField('Star Rating', validators=[DataRequired(), NumberRange(min=1, max=5)])
    submit = SubmitField('Submit Review')


@description_blueprint.route('/description', methods=['GET'])
def description():
    # Get the game_id from the query parameters (e.g., /description?game_id=1)
    game_id = int(request.args.get('game_id'))

    # Retrieve the game details based on the game_id
    game = services.get_game(repo.repo_instance, game_id)

    # Create an instance of the ReviewForm
    form = ReviewForm()

    # Calculate the number of reviews
    length = len(game.reviews)

    # Render the game description page with the form
    return render_template('gameDescription.html', game=game, form=form, length=length)


@description_blueprint.route('/add_review/<int:game_id>', methods=['POST'])
@login_required
def add_review(game_id):
    # Obtain the user name of the currently logged in user.
    user_name = session['user_name']

    # Create an instance of the ReviewForm
    form = ReviewForm()
    game = services.get_game(repo.repo_instance, game_id)

    if form.validate_on_submit():
        # Successful POST, add the review to the game.
        review_text = form.review_text.data

        try:
            # Call the service layer function to add the review
            services.add_review(game_id, review_text, user_name, repo.repo_instance)
            flash('Review posted successfully!', 'success')

        except ValueError as e:
            flash(str(e), 'error')

    # Pass the form instance to the template context for description.html
    return render_template('gameDescription.html', game=game, game_id=game_id, form=form)
