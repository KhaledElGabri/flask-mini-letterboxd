from flask import Blueprint, request, jsonify
from data_service import load_data, save_data
from user import User

user_bp = Blueprint('user_routes', __name__, url_prefix='/users')

_, users = load_data()

# register new user
@user_bp.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    # Check if username exists
    for user in users:
        if user.username == username:
            return jsonify({'error': 'Username already exists'}), 409

    new_user = User(username, password)
    users.append(new_user)
    save_data(users)

    return jsonify({'message': 'User registered successfully', 'user_id': new_user.user_id})


# login user
@user_bp.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    for user in users:
        if user.username == username and user.verify_password(password):
            return jsonify({'message': 'Login successful', 'user_id': user.user_id})

    return jsonify({'error': 'Invalid credentials'}), 401
