from flask import Blueprint, request, jsonify
from data_service import load_users, save_users
from user import User
from utils import get_html

user_bp = Blueprint('user', __name__, url_prefix='/user')

session = {} # in-memory session


# register new user
@user_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        if any(user.username == username for user in users):
            return "Username already exists. Please choose another."
        else:
            new_user = User(
                username=username,
                password=password,
                profile_picture_url='/static/img/default_profile.png'
            )

            users.append(new_user)
            save_users(users)
            session['username'] = username
            return get_html("login")
    else:
        return get_html("signup")


# login user
@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        for user in users:
            if user.username == username and user.password == password:
                session['username'] = username
                return get_html("index")
        return "Invalid username or password."
    else:
        return get_html("login")


# logout user
@user_bp.route('/logout')
def logout():
    if 'username' in session:
        del session['username']
        return get_html("index")
    else:
        return "You are not logged in."