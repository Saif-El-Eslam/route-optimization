from flask import Flask, request, jsonify
from flask_cors import CORS

from services import *
from schemas import *

from auth_handlers import generate_jwt_token, get_user_by_token, hash_password, check_password

app = Flask(__name__)
CORS(app)

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    
    role = data.get('role')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    # check if email already exists
    if get_user_by_email(email):
        return jsonify({'error': 'there is already an account associated with this email'}), 400
        
    password = data.get('password')
    confirm_password = data.get('confirm_password')
    if password != confirm_password:
        return jsonify({'error': 'Passwords do not match'}), 400

    hashed_password = hash_password(password)

    if role == 0:
        verified = True
    elif role == 1:
        verified = False
        bus_number = data.get('bus_number')
        plate_number = data.get('plate_number')

    

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
                'bus_number': bus_number,
                'plate_number': plate_number
            })

            response_data = {
                'role': created_user.role,
                'first_name': created_user.first_name,
                'last_name': created_user.last_name,
                'email': created_user.email,
                'verified': created_user.verified,
                'bus_number': created_user.bus_number,
                'plate_number': created_user.plate_number
            }
        else:
            raise Exception('Invalid role')

        
        return jsonify(response_data), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    try:
        user = get_user_by_email(email)
        
        if user:
            if not check_password(password, user.password):
                return jsonify({'error': 'Invalid credentials'}), 401

            # Generate JWT token
            token = generate_jwt_token(str(user.id))

            try:
                updated_user = update_user(str(user.id), {'token': token})
            except Exception as e:
                return jsonify({'error': str(e)}), 400

            return jsonify({'token': token}), 200
        else:
            return jsonify({'error': 'Invalid credentials'}), 401

    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/logout', methods=['POST'])
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


if __name__ == '__main__':
    app.run()

