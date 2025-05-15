import datetime



class User:
    """
    User Details
    """

    def __init__(self, username, password, profile_picture_url, user_id=None, joined_on=None, movie_watched=None):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.profile_picture_url = profile_picture_url
        self.joined_on = joined_on if joined_on else datetime.date.today()
        self.movie_watched = movie_watched if movie_watched is not None else {}


    # to be implemented
    def _hash_password(self, password):
        pass

    # mark movie as watched
    def marked_movies(self, movie_id, movie_title):
        self.movie_watched[movie_id] = movie_title


    # unmark movie as watched
    def unmarked_movies(self, movie_id):
        if movie_id in self.movie_watched:
            del self.movie_watched[movie_id]

    # generate a new id
    def generate_new_id(exist_user):
        max_user_id = 0
        for user in exist_user:
            if user.user_id and user.user_id.isdigit():
                user_id_int = int(user.user_id)
                if user_id_int > max_user_id:
                    max_user_id = user_id_int

        return str(max_user_id + 1)



    # convert user object to dict (Serialization)
    def to_dict(self):
        return {
            'user_id': self.user_id,
            'username': self.username,
            'password': self.password,
            'profile_picture_url': self.profile_picture_url,
            'joined_on': self.joined_on.isoformat() if isinstance(self.joined_on, (datetime.date, datetime.datetime)) else self.joined_on,
            'movie_watched': self.movie_watched
        }


    # create a user object from dict data (Deserialization)
    @classmethod
    def from_dict(cls, data):
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