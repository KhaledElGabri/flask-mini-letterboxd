import json
import datetime
from user import User

MOVIES_FILE = "data/movies.json"  # pre-populated movies file
USERS_FILE = "data/users.json" # users file
LOGS_FILE = "data/logs-users.txt" # logs file


# loads movie data
def load_movies():
    try:
        with open(MOVIES_FILE, "r") as f:
            return json.load(f)
    except:
        print("Error loading movies")
        return []



# saves movie data
def save_movies(movies):
    try:
        with open(MOVIES_FILE, "w") as f:
            json.dump(movies, f, indent=4)
        print(f"successfully saved {len(movies)} movies to {MOVIES_FILE}")
    except:
        print("error saving movies")


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
        print(f"successfully saved {len(users)} users to {USERS_FILE}")
    except:
        print(f"error saving users")

# log user activity
def user_logs(username, action):
    try:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"At [{timestamp}] the-username: {username}: {action}\n"
        with open(LOGS_FILE, "a") as f:
            f.write(log_entry)
    except:
        print("Error logging")
