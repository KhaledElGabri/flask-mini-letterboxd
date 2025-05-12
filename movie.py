from datetime import datetime


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
        return f"{self.title} directed by {self.director} ({self.year if self.year else 'N/A'})"


    # movie short description.
    def get_short_description(self, length=100):
        if self.description:
            return (self.description[:length] + "...") if len(self.description) > length else self.description
        return ""


    # add a review
    def add_review(self, user_id, username, text):
        review = {
            'user_id': user_id,
            'username': username,
            'text': text,
            'rating': None,
            'created_at': datetime.now().isoformat()
        }
        self.reviews.append(review)
        return True


    # add a rating
    def add_rating(self, user_id, rating):
        self.user_ratings[user_id] = rating
        self._update_average_rating()

        for review in self.reviews:
            if review['user_id'] == user_id:
                review['rating'] = rating
                break
        return True


    # update average rating
    def _update_average_rating(self):
        if not self.user_ratings:
            self.rating = None
        else:
            self.rating = sum(self.user_ratings.values()) / len(self.user_ratings)


    # update a review
    def update_review(self, user_id, new_text=None, new_rating=None):
        for review in self.reviews:
            if review['user_id'] == user_id:
                if new_text is not None:
                    review['text'] = new_text

                # update rating
                if new_rating is not None:
                    review['rating'] = new_rating
                    self.user_ratings[user_id] = new_rating
                    self._update_average_rating()

                return True
        return False


    # delete a review
    def delete_review(self, user_id):
        for i, review in enumerate(self.reviews):
            if review['user_id'] == user_id:
                self.reviews.pop(i)

                # remove rating if exists
                if user_id in self.user_ratings:
                    del self.user_ratings[user_id]
                    self._update_average_rating()

                return True
        return False




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
            'user_ratings': self.user_ratings
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