from flask import Flask
from routes.movie_routes import movie_bp
from utils import get_html
from data_service import load_movies

app = Flask(__name__, static_folder='static')


# register Blueprints
app.register_blueprint(movie_bp)

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
        movie_items.append(item)

    movies_grid = "".join(movie_items)
    return get_html("index").replace("$$MOVIES$$", f'<div id="movie-list">{movies_grid}</div>')


if __name__ == '__main__':
    app.run(debug=True)
