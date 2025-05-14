from flask import Blueprint, jsonify
# from data_service import load_movies

movie_bp = Blueprint('movie_routes', __name__, url_prefix='/movies')
