import datetime



class User:
    """
    User Details
    """

    def __init__(self, username, password, user_id=None, profile_picture_url="", joined_on=None, movie_watched=None):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.profile_picture_url = profile_picture_url
        self.joined_on = joined_on if joined_on else datetime.date.today()
        self.movie_watched = movie_watched if movie_watched is not None else {}


    # to be implemented
    def _hash_password(self, password):
        pass


    # get user profile link
    def get_profile_link(self):
        return self.username


    # mark movie as watched
    def marked_movies(self, movie_id, movie_title):
        self.movie_watched[movie_id] = movie_title


    # unmark movie as watched
    def unmarked_movies(self, movie_id):
        if movie_id in self.movie_watched:
            del self.movie_watched[movie_id]


    # convert user object to dict (Serialization)
    def to_dict(self):
        return {
            'user_id': self.username, # saves the username as id temporary
            'username': self.username,
            'password': self.password,
            'profile_picture_url': self.profile_picture_url,
            'joined_on': self.joined_on.isoformat() if isinstance(self.joined_on, (datetime.date, datetime.datetime)) else self.joined_on,
            'movie_watched': self.movie_watched
        }


    # create a user object from dict data (Deserialization)
    @classmethod
    def from_dict(cls, data):
        if 'username' not in data:
            print("username key error")
            return None

        joined_str = data.get('joined_on')
        joined_date = datetime.date.fromisoformat(joined_str) if joined_str else None
        return cls(
            user_id=data.get('user_id'),
            username=data.get('username'),
            password=data.get('password'),
            profile_picture_url=data.get('profile_picture_url'),
            joined_on=joined_date,
            movie_watched=data.get('movie_watched', {})
        )