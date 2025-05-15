from flask import Blueprint, request, session, redirect, url_for
from data_service import load_users, save_users
from user import User
from utils import get_html

user_bp = Blueprint('user', __name__, url_prefix='/user')


# register new user
@user_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()

        username_exist = False
        for user in users:
            if user.username == username:
                username_exist = True
                break

        if username_exist:
            print(f"username '{username}' exists")
            return get_html("signup")
        else:
            new_user_id = User.generate_new_id(users)
            new_user = User(
                user_id=new_user_id,
                username=username,
                password=password,
                profile_picture_url='/static/img/default_profile.png'
            )
            users.append(new_user)
            save_users(users)

            session['username'] = username
            session.permanent = True
            return redirect(url_for('user.profile'))
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
                session.permanent = True
                return redirect(url_for('user.profile'))

        print(f"invalid login for username -> {username}")
        return get_html("login")
    else:
        return get_html("login")


# logout user
@user_bp.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))



# user profile
@user_bp.route('/profile')
def profile():
    pass
