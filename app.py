from flask import Flask, session
from routes.movie_routes import movie_bp
from routes.user_routes import user_bp
from utils import get_html
from data_service import load_movies

app = Flask(__name__, static_folder='static')


app.secret_key = 'secret_key'
app.permanent_session_lifetime = 20 * 60

# register Blueprints
app.register_blueprint(movie_bp)
app.register_blueprint(user_bp)


@app.route('/')
def home():
    movies = load_movies()
    movie_items = []
    for movie_id, movie in movies.items():
        item = f'''<div class="movie-grid-item">
                <a href="/movies/{movie.get('movie_id', movie_id)}">
                    <img src="{movie['poster_url']}" class="movie-poster">
                </a>
            </div>'''
        # print(movie) # debugging
        movie_items.append(item)

    movies_grid = "".join(movie_items)

    is_logged_in = 'username' in session
    index_html = get_html("index")
    if is_logged_in:
        user_auth_links = f'''
        <nav class="auth-links">
            <a href="/user/logout" class="log-out" id="logout-btn">Logout</a>
        </nav>
        '''
    else:
        user_auth_links = '''
        <nav class="auth-links">
            <a href="/user/login" class="log-in">Login</a>
            <a href="/user/signup" class="sign-up">Sign Up</a>
        </nav>
        '''

    index_html = index_html.replace("$$AUTH_LINKS$$", user_auth_links)
    index_html = index_html.replace("$$MOVIES$$", f'<div id="movie-list">{movies_grid}</div>')

    return index_html


# handle all not found pages
@app.errorhandler(404)
def page_not_found(e):
    return get_html("not_found"), 404

if __name__ == '__main__':
    app.run(debug=True)