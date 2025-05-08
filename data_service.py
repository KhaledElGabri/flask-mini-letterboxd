import json
from movie import Movie
from user import User
import os

DATA_FILE = "data.json"  # save user data file
MOVIES_DATA_FILE = "data/movies.json"  # pre-populated movies file

def load_data():
    movies = _load_movies()
    users = _load_users()
    return movies, users

def _load_movies():
    try:
        with open(MOVIES_DATA_FILE, 'r') as f:
            movie_data = json.load(f)
            # Assuming your movies.json is a dictionary where keys are movie IDs
            movies = [Movie.from_dict(data) for data in movie_data.values()]
        return movies
    except FileNotFoundError:
        print(f"Movies data file '{MOVIES_DATA_FILE}' not found. Starting with no movies.")
        return []
    except json.JSONDecodeError:
        print(f"Error decoding JSON from '{MOVIES_DATA_FILE}'. Starting with no movies.")
        return []
    except Exception as e:
        print(f"An unexpected error occurred while loading movies: {e}. Starting with no movies.")
        return []

def _load_users():
    try:
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
            users = [User.from_dict(user_data) for user_data in data.get('users', [])]
        return users
    except FileNotFoundError:
        print(f"Users data file '{DATA_FILE}' not found. Starting with no users.")
        return []
    except json.JSONDecodeError:
        print(f"Error decoding JSON from '{DATA_FILE}'. Starting with no users.")
        return []
    except Exception as e:
        print(f"An unexpected error occurred while loading users: {e}. Starting with no users.")
        return []


def save_data(users):
    try:
        data = {
            'users': [user.to_dict() for user in users]
        }
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"User data saved successfully to '{DATA_FILE}'")
    except Exception as e:
        print(f"Error saving user data to '{DATA_FILE}': {e}")