from flask import Blueprint, request, session, redirect, url_for
from data_service import load_users, save_users, user_logs
from user import User
from utils import get_html


user_bp = Blueprint('user', __name__, url_prefix='/user')



# validate the password
def validate_pass(password):
    if len(password) < 6:
        return "Password must be at least 6 characters"

    if not any(char.isdigit() for char in password):
        return "Password must contain at least one number"

    special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?/"
    if not any(char in special_chars for char in password):
        return "Password must contain at least one special character"

    return None


# register new user
@user_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        pass_err = validate_pass(password)
        if pass_err:
            signup_html = get_html("signup")
            signup_html = signup_html.replace('<p id="password-error" class="error-message" style="color: red; display: none;">',
                                              f'<p id="password-error" class="error-message" style="color: red;">')
            return signup_html

        users = load_users()
        username_exist = False
        for user in users:
            if user.username == username:
                username_exist = True
                break

        if username_exist:
            print(f"Username '{username}' already exists")
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
            user_logs(username, "created account")
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
            temp_user = User("temp", password, "")
            hashed_password = temp_user._hash_password_FNV1a_64(password)

            if user.username == username and (user.password == hashed_password or user.password == password):
                session['username'] = username
                session.permanent = True
                user_logs(username, "logged in") # log activity

                # set LocalStorage before redirect
                return f"""
                <script>
                    localStorage.setItem("username", "{username}");
                    window.location.href = "{url_for('home')}";
                </script>
                """

        login_html = get_html("login")
        login_html = login_html.replace(
            '<p id="login-error" class="error-message" style="color: red; display: none;">',
            '<p id="login-error" class="error-message" style="color: red;">'
        )
        login_html = login_html.replace(
            'Invalid username or password.',
            'Invalid username or password. Please try again.'
        )
        return login_html
    else:
        return get_html("login")


# logout user
@user_bp.route('/logout')
def logout():
    username = session.get('username')
    if username:
        user_logs(username, "logged out")
    session.clear()  # clear the entire session

    # clear LocalStorage before redirect
    return """
    <script>
        localStorage.removeItem("username");
        window.location.replace("/");
    </script>
    """


# user profile
@user_bp.route('/profile')
def profile():
    pass
