
class Movie:
    """
    Movie Details
    """

    def __init__(self, movie_id, title, director, year, rating, description, poster_url, reviews=None):
        self.movie_id = movie_id
        self.title = title
        self.director = director
        self.year = year
        self.rating = rating
        self.description = description
        self.poster_url = poster_url
        self.reviews = reviews if reviews is not None else {}
        # self.user_ratings = user_ratings if user_ratings is not None else {}



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
            'reviews': self.reviews,
            # 'user_ratings': self.user_ratings
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
            reviews=data.get('reviews', {}),
            # user_ratings=data.get('user_ratings', {})
        )