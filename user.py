import uuid
from datetime import datetime
import hashlib


class User:
    """
    User Details
    """

    def __init__(self, username, password, user_id=None, profile_picture_url="", joined_on=None, watched=None):
        self.user_id = user_id if user_id else str(uuid.uuid4())
        self.username = username
        self.password = self._hash_password(password)
        self.profile_picture_url = profile_picture_url
        self.joined_on = joined_on or datetime.now().isoformat()
        self.watched = watched if watched is not None else []


    # Hashes the given password using SHA-256
    def _hash_password(self, password):
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        return hashed_password


    # verifying user password
    def verify_password(self, pass_attempt):
        attempt = self._hash_password(pass_attempt)
        return self.password == attempt


    # get user profile link
    def get_profile_link(self):
        return self.username




    # convert user object to dict (Serialization)
    def to_dict(self):
        return {
            'user_id': self.user_id,
            'username': self.username,
            'password': self.password,
            'profile_picture_url': self.profile_picture_url,
            'joined_on': self.joined_on,
            'watchlist': self.watchlist,
            'watched': self.watched
        }


    # create a user object from dict data (Deserialization)
    @classmethod
    def from_dict(cls, data):
        user = cls(
            username=data['username'],
            password="placeholder",
            profile_picture_url=data.get('profile_picture_url', ""),
            user_id=data.get('user_id'),
            joined_on=data.get('joined_on'),
            watched=data.get('watched')
        )
        user.password = data['password']
        return user