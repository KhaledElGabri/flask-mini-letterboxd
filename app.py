from flask import Flask
from routes import movie_routes

app = Flask(__name__)


# register Blueprints
app.register_blueprint(movie_routes.bp)

@app.route('/')
def home_page():
    return 'Hello, RemoteCoders!'


if __name__ == '__main__':
    app.run(debug=True)
