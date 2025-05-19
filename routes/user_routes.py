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


# validate the username
def validate_username(username):
    if len(username) < 3:
        return "Username must be at least 3 characters"
    
    if len(username) > 30:
        return "Username cannot exceed 30 characters"


    if username.isdigit():
        return "Username cannot contain only numbers"

    chars_count = sum(1 for char in username if char.isalpha())
    if chars_count < 3:
        return "Username must contain at least 3 alphabetic characters"
    
    if '@' in username and '.' in username.split('@')[1]:
        return "Email addresses are not allowed as usernames. Please use a regular username."
    
    return None


# register new user
@user_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # validate username
        username_err = validate_username(username)
        if username_err:
            signup_html = get_html("signup")
            signup_html = signup_html.replace('<p id="password-error" class="error-message" style="color: red; display: none;">',
                                              f'<p id="password-error" class="error-message" style="color: red;">{username_err}</p>')
            return signup_html

        # validate password
        pass_err = validate_pass(password)
        if pass_err:
            signup_html = get_html("signup")
            signup_html = signup_html.replace('<p id="password-error" class="error-message" style="color: red; display: none;">',
                                              f'<p id="password-error" class="error-message" style="color: red;">{pass_err}</p>')
            return signup_html

        users = load_users()
        username_exist = False
        lowercase_username = username.lower()
        
        for user in users:
            if user.username.lower() == lowercase_username:
                username_exist = True
                break

        if username_exist:
            signup_html = get_html("signup")
            signup_html = signup_html.replace('<p id="password-error" class="error-message" style="color: red; display: none;">',
                                             f'<p id="password-error" class="error-message" style="color: red;">Username already exists. Please choose another one.</p>')
            return signup_html
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

            if user.username.lower() == username.lower() and user.password == hashed_password:
                session['username'] = user.username
                session.permanent = True
                user_logs(user.username, "logged in")

                # set LocalStorage before redirect
                return f"""
                <script>
                    localStorage.setItem("username", "{user.username}");
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
    session.clear() # clear entire session

    # clear LocalStorage before redirect
    return """
    <script>
        localStorage.removeItem("username");
        window.location.replace("/");
    </script>
    """


# user profile functionalities
@user_bp.route('/profile')
def profile():
    if 'username' not in session:
        return redirect(url_for('user.login'))

    username = session['username']
    user = find_user_by_username(username)

    if not user:
        not_found_html = get_html("not_found")
        return not_found_html, 404

    return render_user_profile(user)


@user_bp.route('/profile/<user_id>')
def user_profile_by_id(user_id):
    users = load_users()
    user = None
    for usr in users:
        if usr.user_id == user_id:
            user = usr
            break

    if not user:
        not_found_html = get_html("not_found")
        return not_found_html, 404

    return render_user_profile(user)


def find_user_by_username(username):
    users = load_users()
    for user in users:
        if user.username.lower() == username.lower():
            return user
    return None



# render the user profile info
def render_user_profile(user):
    profile_html = get_html("profile")

    watched_movies_html = ""
    if user.movie_watched:
        for movie_id, movie_title in user.movie_watched.items():
            watched_movies_html += f'<div class="movie-entry"> <p>Watched <a href="/movies/{movie_id}">{movie_title}</a> </p> </div>'
    else:
        watched_movies_html = '<p class="no-movies-message">No movies watched yet.</p>'

    replacements = {
        '$$USERNAME$$': user.username,
        '$$JOINED_DATE$$': user.joined_on.strftime("%B %d, %Y"),
        '$$WATCHED_COUNT$$': str(len(user.movie_watched)),
        '$$PROFILE_PIC$$': user.profile_picture_url,
        '$$WATCHED_MOVIES$$': watched_movies_html
    }

    for placeholder, val in replacements.items():
        profile_html = profile_html.replace(placeholder, val)

    return profile_html
