from flask import Blueprint, request, render_template, session
from games.adapters.memory_repository import *
from games.user import wishlist, services

def get_user_reviews():
        user_name = session.get('user_name')
        current_user = services.get_user(repo.repo_instance, user_name)
        reviews = current_user.reviews
        return reviews

