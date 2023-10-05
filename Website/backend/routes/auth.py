from flask import Flask, request, jsonify

from services import *
from schemas import *

from token_handlers import generate_jwt_token, get_user_by_token

app = Flask(__name__)

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()

    username = data.get('username')
    email = data.get('email')
    phone_number = data.get('phone_number')
    password = data.get('password')
    role = data.get('role')
    license_number = data.get('license_number')

    try: 
        created_user = create_user({
            'username': username,
            'email': email,
            'phone_number': phone_number,
            'password': password,
            'role': role,
            'license_number': license_number,
            'verified': False
        })

        response_data = {
            'username': created_user.username,
            'email': created_user.email,
            'phone_number': created_user.phone_number,
            'role': created_user.role,
            'license_number': created_user.license_number,
            'verified': created_user.verified
        }
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
        print(user)
        if user:
            try:
                updated_user = update_user(str(user.id), {'token': ''})
            except Exception as e:
                return jsonify({'error': str(e)}), 400

            return jsonify({'message': 'Logged out successfully'}), 200
        else:
            return jsonify({'error': 'Invalid token'}), 401
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    app.run()

