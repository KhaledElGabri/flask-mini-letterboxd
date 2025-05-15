import json
# from movie import Movie
from user import User
# import os

MOVIES_FILE = "data/movies.json"  # pre-populated movies file
USERS_FILE = "data/users.json" # users file


# loads movie data
def load_movies():
    try:
        with open(MOVIES_FILE, "r") as f:
            return json.load(f)
    except:
        print(f"Error loading movies from {MOVIES_FILE}")
        return []



# saves movie data
def save_movies(movies):
    pass

def load_users():
    try:
        with open(USERS_FILE, "r") as f:
            user_data = json.load(f)
        users = []
        for data in user_data:
            user = User.from_dict(data)
            if user:
                users.append(user)
        print(f"successfully loaded {len(users)} users from {USERS_FILE}")
        return users
    except:
        print(f"error loading users")
        with open(USERS_FILE, "w") as f:
            f.write("[]")
        return []

# saves users data
def save_users(users):
    try:
        user_dicts = [user.to_dict() if isinstance(user, User) else user for user in users]
        with open(USERS_FILE, "w") as f:
            json.dump(user_dicts, f, indent=4)
        print(f"Successfully saved {len(users)} users to {USERS_FILE}")
    except Exception as e:
        print(f"Error saving users: {e}")