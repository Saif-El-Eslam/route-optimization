from flask import Blueprint, request, jsonify

from services import *
from schemas import *

from auth_handlers import generate_jwt_token, get_user_by_token, hash_password, check_password

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    
    role = data.get('role')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    # check if email already exists
    if get_user_by_email(email):
        return jsonify({'error': 'Email already exists'}), 400

    password = data.get('password')
    confirm_password = data.get('confirm_password')
    if password != confirm_password:
        return jsonify({'error': 'Passwords do not match'}), 400

    hashed_password = hash_password(password)

    if role == 0:
        verified = True
    elif role == 1:
        verified = False
        bus_id = data.get('bus_id')
        license_number = data.get('license_number')

    try: 
        if role == 0:
            created_user = create_user({
                'role': role,
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'password': hashed_password,
                'verified': verified

            })

            response_data = {
                'role': created_user.role,
                'first_name': created_user.first_name,
                'last_name': created_user.last_name,
                'email': created_user.email,
                'verified': created_user.verified
            }
        elif role == 1:
            created_user = create_user({
                'role': role,
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'password': hashed_password,
                'verified': verified,
                'bus_id': bus_id,
                'license_number': license_number
            })

            response_data = {
                'role': created_user.role,
                'first_name': created_user.first_name,
                'last_name': created_user.last_name,
                'email': created_user.email,
                'verified': created_user.verified,
                'bus_id': created_user.bus_id,
                'license_number': created_user.license_number
            }
        else:
            raise Exception('Invalid role')

        
        return jsonify(response_data), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 400


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    try:
        user = get_user_by_email(email)
        if user:
            if not check_password(password, user.password):
                return jsonify({'error': 'Invalid credentials'}), 401

            if user.role == 1 and not user.verified:
                return jsonify({'error': 'Driver is not verified yet'}), 401

            # Generate JWT token
            token = generate_jwt_token(str(user.id))

            try:
                updated_user = update_user(str(user.id), {'token': token})
            except Exception as e:
                return jsonify({'error': str(e)}), 400
            
            return jsonify({
                'token': token,
                'role': updated_user.role,
                'first_name': updated_user.first_name,
                'last_name': updated_user.last_name,
            }), 200
        else:
            return jsonify({'error': 'Invalid credentials'}), 401

    except Exception as e:
        return jsonify({'error': str(e)}), 400


@auth_bp.route('/logout', methods=['POST'])
def logout():
    bearer_token = request.headers.get('Authorization')
    token = bearer_token.split(' ')[1]

    try:
        user = get_user_by_token(token)
        if user.token and user.token != "":
            try:
                updated_user = update_user(str(user.id), {'token': ''})
            except Exception as e:
                return jsonify({'error': str(e)}), 400

            return jsonify({'message': 'Logged out successfully'}), 200
        else:
            return jsonify({'error': 'User is not logged in'}), 400
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400
