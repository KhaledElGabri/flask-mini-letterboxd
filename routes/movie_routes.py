from flask import Blueprint, request, redirect, url_for, session
from data_service import load_movies, load_users, save_users, save_movies
from utils import get_html
from datetime import datetime


movie_bp = Blueprint('movie', __name__, url_prefix='/movies')


# get the current user from the session
def get_current_user():
    users = load_users()
    username = session.get('username')
    if not username:
        return None

    for user in users:
        if user.username == username:
            return user

    session.clear()
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

    movie = check_movie_by_id(movies, movie_id)
    if not movie:
        not_found_html = get_html("not_found")
        return not_found_html, 404

    # POST request handling
    if request.method == 'POST':
        if user is None:
            return status_of_user()

        # delete review request
        if request.form.get('action') == 'delete_review':
            review_id = request.form.get('review_id')
            if review_id:
                delete_review(movie_id, review_id)
            return redirect(url_for('movie.movie_detail', movie_id=movie_id))

        # edit review request
        elif request.form.get('action') == 'edit_review':
            review_id = request.form.get('review_id')
            if review_id:
                return get_edit_review_form(movie_id, review_id)

        # edit review submission
        elif request.form.get('action') == 'update_review':
            review_id = request.form.get('review_id')
            updated_text = request.form.get('review_text', '').strip()
            if review_id and updated_text:
                update_review(movie_id, review_id, updated_text)
            return redirect(url_for('movie.movie_detail', movie_id=movie_id))

        # watched request
        elif 'review_text' not in request.form:
            for usr in users:
                if usr.username == user.username:
                    if movie_id in usr.movie_watched:
                        unmark_as_watched(movie_id, usr)
                    else:
                        mark_as_watched(movie_id, usr, movie['title'])
                    break
            save_users(users)
            return redirect(url_for('movie.movie_detail', movie_id=movie_id))

        else:
            review_text = request.form.get('review_text', '').strip()
            if review_text:
                add_review(movie_id, user, review_text)

        return redirect(url_for('movie.movie_detail', movie_id=movie_id))

    # render html
    movie_detail_html = get_html("movie_detail")
    reviews_html = get_all_movie_reviews(movie, user)

    replacements = {
        '$$TITLE$$': movie['title'],
        '$$POSTER_URL$$': movie['poster_url'],
        '$$DIRECTOR$$': movie['director'],
        '$$YEAR$$': str(movie['year']),
        '$$RATING$$': str(movie['rating']) if movie['rating'] is not None else "N/A",
        '$$DESCRIPTION$$': movie['description'],
        '$$REVIEWS$$': reviews_html,
    }

    btn_text = "Mark as Watched"
    if user and movie_id in user.movie_watched:
        btn_text = "Watched"
    replacements['$$MARK_AS_WATCHED$$'] = btn_text

    for placeholder, val in replacements.items():
        movie_detail_html = movie_detail_html.replace(placeholder, val)
    return movie_detail_html


# search
@movie_bp.route('/search')
def search_movies():
    query = request.args.get('query', '').lower()
    if not query:
        return redirect(url_for('home'))

    movies = load_movies()
    filtered_movies = {}

    for movie_id, movie in movies.items():
        if query in movie['title'].lower():
            filtered_movies[movie_id] = movie

    # filtered movies
    movie_items = []
    for movie_id, movie in filtered_movies.items():
        item = f'''<div class="movie-grid-item">
                <a href="/movies/{movie.get('movie_id', movie_id)}">
                    <img src="{movie['poster_url']}" class="movie-poster">
                </a>
            </div>'''
        movie_items.append(item)

    index_html = get_html("index")
    is_logged_in = 'username' in session

    # replace auth links based on login status
    if is_logged_in:
        auth_links = '''
        <nav class="auth-links">
            <a href="/user/logout" class="log-out" id="logout-btn" >Logout</a>
        </nav>
        '''
    else:
        auth_links = '''
        <nav class="auth-links">
            <a href="/user/login" class="log-in">Login</a>
            <a href="/user/signup" class="sign-up">Sign Up</a>
        </nav>
        '''

    index_html = index_html.replace("$$AUTH_LINKS$$", auth_links)
    if not movie_items:
        no_results = '<div>No movies found matching your search.</div>'
        return index_html.replace("$$MOVIES$$", no_results)

    movies_grid = "".join(movie_items)
    return index_html.replace("$$MOVIES$$", f'<div id="movie-list">{movies_grid}</div>')


# marked as watched
def mark_as_watched(movie_id, user, movie_title):
    user.marked_movies(movie_id, movie_title)

# marked as watched
def unmark_as_watched(movie_id, user):
    user.unmarked_movies(movie_id)


# add review feature
def add_review(movie_id, user, review_text):
    movies = load_movies()
    movie = check_movie_by_id(movies, movie_id)
    if movie is None:
        return False

    if 'reviews' not in movie:
        movie['reviews'] = {}

    review_id = new_rev_id(movie) # generate unique review ID

    movie['reviews'][review_id] = {
        'review_id': review_id,
        'user_id': user.user_id,  # use actual user id instead of username
        'username': user.username,
        'review_text': review_text,
        'date': datetime.now().strftime("%Y-%m-%d")
    }

    save_movies(movies)
    return True

def new_rev_id(movie):
    max_id = 0
    if 'reviews' in movie:
        for review_id, review in movie['reviews'].items():
            # Check if the review_id is numeric
            if review_id.isdigit():
                review_id_int = int(review_id)
                if review_id_int > max_id:
                    max_id = review_id_int

    return str(max_id + 1)


# get all reviews with delete and edit btns
def get_all_movie_reviews(movie, current_user=None):
    if not movie or 'reviews' not in movie or not movie['reviews']:
        return "<p class='no-reviews'>No reviews yet. Be the first to share your thoughts!</p>"

    reviews_html = ""
    for review_id, review in movie['reviews'].items():
        del_btn = ""
        edit_btn = ""

        if current_user is None:
            current_user = get_current_user()

        # check current user author of review
        owner_review = current_user and current_user.user_id == review['user_id']
        if owner_review:
            edit_btn = f"""
            <form method="POST" class="edit-review-form">
                <input type="hidden" name="action" value="edit_review">
                <input type="hidden" name="review_id" value="{review_id}">
                <button class="edit-button" type="submit">Edit</button>
            </form>
            """
            del_btn = f"""
            <form method="POST" class="del-review-form">
                <input type="hidden" name="action" value="delete_review">
                <input type="hidden" name="review_id" value="{review_id}">
                <button class="del-button" type="submit">Delete</button>
            </form>
            """
        review_temp = f"""
        <div class="review" id="review-{review_id}">
            <div class="review-header">
                <span class="username">Reviewed by <span class="user-style">{review['username']}</a></span></span>
                <span class="date">{review.get('date', 'Unknown date')}</span>
            </div>
            <div class="review-text">
                <div>{review['review_text']}</div>
                <div class="review-actions">
                    {edit_btn}
                    {del_btn}
                </div>
            </div>
        </div>
        """
        reviews_html += review_temp
    return reviews_html

# delete a review if user is authorized
def delete_review(movie_id, review_id):
    user = get_current_user()
    if not user:
        return False

    movies = load_movies()
    movie = check_movie_by_id(movies, movie_id)

    if movie and 'reviews' in movie and review_id in movie['reviews']:
        if movie['reviews'][review_id]['user_id'] == user.user_id:
            del movie['reviews'][review_id]
            save_movies(movies)
            return True
        else:
            return False
    else:
        return False

#  show a form to edit a review
def get_edit_review_form(movie_id, review_id):
    user = get_current_user()
    if not user:
        return status_of_user()

    movies = load_movies()
    movie = check_movie_by_id(movies, movie_id)

    if not movie or 'reviews' not in movie or review_id not in movie['reviews']:
        not_found_html = get_html("not_found")
        return not_found_html, 404

    review = movie['reviews'][review_id]

    # if current user is author of the review
    if review['user_id'] != user.user_id:
        return redirect(url_for('movie.movie_detail', movie_id=movie_id))

    movie_detail_html = get_html("movie_detail")
    edit_form = f"""
    <div class="review-section">
        <div class="reviews-header">
            <h2>Edit Your Review</h2>
        </div>
        <form class="review-form" method="POST" action="">
            <input type="hidden" name="action" value="update_review">
            <input type="hidden" name="review_id" value="{review_id}">
            <textarea class="review-area" name="review_text" rows="5">{review['review_text']}</textarea>
            <button type="submit" class="log-review-btn">Update</button>
            <a href="/movies/{movie_id}" class="cancel-btn">Cancel</a>
        </form>
    </div>
    """

    replacements = {
        '$$TITLE$$': movie['title'],
        '$$POSTER_URL$$': movie['poster_url'],
        '$$DIRECTOR$$': movie['director'],
        '$$YEAR$$': str(movie['year']),
        '$$RATING$$': str(movie['rating']) if movie['rating'] is not None else "N/A",
        '$$DESCRIPTION$$': movie['description'],
        '$$REVIEWS$$': edit_form,
    }

    btn_text = "Mark as Watched"
    if user and movie_id in user.movie_watched:
        btn_text = "Watched"
    replacements['$$MARK_AS_WATCHED$$'] = btn_text

    for placeholder, val in replacements.items():
        movie_detail_html = movie_detail_html.replace(placeholder, val)

    return movie_detail_html

def update_review(movie_id, review_id, updated_text):
    user = get_current_user()
    if not user:
        return False

    movies = load_movies()
    movie = check_movie_by_id(movies, movie_id)

    if movie and 'reviews' in movie and review_id in movie['reviews']:
        if movie['reviews'][review_id]['user_id'] == user.user_id:
            movie['reviews'][review_id]['review_text'] = updated_text
            movie['reviews'][review_id]['date'] = datetime.now().strftime("%Y-%m-%d") + " (edited)"
            save_movies(movies)
            return True

    return False