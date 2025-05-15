from flask import Blueprint, request, redirect, url_for, session
from data_service import load_movies, load_users, save_users
from utils import get_html


movie_bp = Blueprint('movie_routes', __name__, url_prefix='/movies')



def get_current_user():
    users = load_users()
    username = session.get('username')
    if username:
        # normal
        for user in users:
            if user.username == username:
                print(user.username)
                return user
    return None

def status_of_user():
    user = get_current_user()
    if user is None:
        login_html = get_html("login")
        return login_html, 401
    return user

def check_movie_by_id(movies, movie_id):
    for mov_id, movie in movies.items():
        if movie.get('movie_id') == movie_id or mov_id == movie_id:
            return movie
    return None

@movie_bp.route('/<movie_id>', methods=['GET', 'POST'])
def movie_detail(movie_id):
    movies = load_movies()
    users = load_users()
    user = get_current_user()

    # check the movie first
    movie = check_movie_by_id(movies, movie_id)
    if not movie:
        not_found_html = get_html("not_found")
        return not_found_html, 404

    # POST request handling
    if request.method == 'POST':
        if user is None:
            return status_of_user()

        # Check if this is a watched toggle request (no review text)
        if 'review_text' not in request.form:
            for usr in users:
                if usr.username == user.username:
                    if movie_id in usr.movie_watched:
                        unmark_as_watched(movie_id, usr)
                    else:
                        mark_as_watched(movie_id, usr, movie['title'])
                    break
            save_users(users)
        else:
            print("Error")
        return redirect(url_for('movie.movie_detail', movie_id=movie_id))

    # render html
    movie_detail_html = get_html("movie_detail")



    replacements = {
        '$$TITLE$$': movie['title'],
        '$$POSTER_URL$$': movie['poster_url'],
        '$$DIRECTOR$$': movie['director'],
        '$$YEAR$$': str(movie['year']),
        '$$RATING$$': str(movie['rating']) if movie['rating'] is not None else "N/A",
        '$$DESCRIPTION$$': movie['description']
    }

    button_text = "Mark as Watched"
    if user and movie_id in user.movie_watched:
        button_text = "Watched"
    replacements['$$MARK_AS_WATCHED$$'] = button_text

    for placeholder, val in replacements.items():
        movie_detail_html = movie_detail_html.replace(placeholder, val)
    return movie_detail_html


def mark_as_watched(movie_id, user, movie_title):
    user.marked_movies(movie_id, movie_title)

def unmark_as_watched(movie_id, user):
    user.unmarked_movies(movie_id)
