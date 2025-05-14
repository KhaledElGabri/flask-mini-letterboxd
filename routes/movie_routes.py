from flask import Blueprint, jsonify
from data_service import load_data

movie_bp = Blueprint('movie', __name__, url_prefix='/movies')
