from flask import Blueprint, jsonify
from data_service import load_data

movie_bp = Blueprint('movie_routes', __name__, url_prefix='/movies')
movies, _ = load_data()

@movie_bp.route('/', methods=['GET'])
def get_all_movies():
    return jsonify([movie.to_dict() for movie in movies])