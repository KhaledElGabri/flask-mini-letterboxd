

class Movie:
    """
    Movie Details
    """

    def __init__(self, title, director, year, movie_id, rating, description, poster_url, reviews=None,user_ratings=None):
        self.movie_id = movie_id
        self.title = title
        self.director = director
        self.year = int(year) if year else None
        self.rating = rating
        self.description = description
        self.poster_url = poster_url
        self.reviews = reviews if reviews is not None else []
        self.user_ratings = user_ratings if user_ratings is not None else {}


    # display the movie info
    def display_info(self):
        pass


    # movie short description.
    def get_short_description(self, length=100):
        pass

    # add a review
    def add_review(self, user_id, username, text):
        pass

    # add a rating
    def add_rating(self, user_id, rating):
        pass

    # update average rating
    def _update_average_rating(self):
        pass

    # update a review
    def update_review(self, user_id, new_text=None, new_rating=None):
        pass


    # delete a review
    def delete_review(self, user_id):
        pass




    # convert movie object to dict (Serialization)
    def to_dict(self):
        return {
            'movie_id': self.movie_id,
            'title': self.title,
            'director': self.director,
            'year': self.year,
            'rating': self.rating,
            'description': self.description,
            'poster_url': self.poster_url,
            'reviews': self.reviews
        }


    # create a Movie object from dict data (Deserialization)
    @classmethod
    def from_dict(cls, data):
        return cls(
            movie_id=data.get('movie_id'),
            title=data.get('title'),
            director=data.get('director'),
            year=data.get('year'),
            rating=data.get('rating'),
            description=data.get('description'),
            poster_url=data.get('poster_url'),
            reviews=data.get('reviews', []),
            user_ratings=data.get('user_ratings', {})
        )