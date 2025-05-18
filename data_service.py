import json
import datetime
import os
from user import User

MOVIES_FILE = "data/movies.json"  # pre-populated movies file
USERS_FILE = "data/users.json" # users file
LOGS_FILE = "data/logs-users.txt" # logs file


# loads movie data
def load_movies():
    if os.path.exists(MOVIES_FILE):
        f = open(MOVIES_FILE, "r")
        movies = json.load(f)
        f.close()
        return movies
    else:
        return []



# saves movie data
def save_movies(movies):
    with open(MOVIES_FILE, "w") as f:
        json.dump(movies, f, indent=4)


def load_users():
    if os.path.exists(USERS_FILE):
        f = open(USERS_FILE, "r")
        users_data = json.load(f)
        f.close()
        users = []
        for data in users_data:
            user = User.from_dict(data)
            if user:
                users.append(user)
        return users
    else:
        f = open(USERS_FILE, "w")
        f.write("[]")
        f.close()
        return []

# saves users data
def save_users(users):
    users_dicts = [user.to_dict() if isinstance(user, User) else user for user in users]
    f = open(USERS_FILE, "w")
    json.dump(users_dicts, f, indent=4)
    f.close()

# log user activity
def user_logs(username, action):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logs = f"At [{timestamp}] the-username: {username}: {action}\n"
    f = open(LOGS_FILE, "a")
    f.write(logs)
    f.close()
