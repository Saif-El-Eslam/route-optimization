from flask import Blueprint, request, jsonify
from flask_cors import CORS

from services import *
from schemas import *
from auth_handlers import get_user_by_token

admin_requests_bp = Blueprint('admin_requests_bp', __name__)

@admin_requests_bp.route('/not-verified-users', methods=['GET'])
def get_not_verified_users():
    bearer_token = request.headers.get('Authorization')
    token = bearer_token.split(' ')[1]

    try:
        user = get_user_by_token(token)
        if not user:
            return jsonify({'error': 'Invalid token'}), 401

        if user.role != 2:
            return jsonify({'error': 'User is Unauthorized'}), 403

        users = get_users_by_role(1)
        response_data = []
        for user in users:
            response_data.append({
                'user_id': str(user.id),
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'license_number': user.license_number,
                'verified': user.verified
            })


        return jsonify(response_data), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400

    
@admin_requests_bp.route('/verify-user', methods=['POST'])
def verify_user():
    bearer_token = request.headers.get('Authorization')
    token = bearer_token.split(' ')[1]

    data = request.get_json()
    verify = data.get('verify')
    user_id = data.get('user_id')

    try:
        admin = get_user_by_token(token)
        if not admin:
            return jsonify({'error': 'Invalid token for admin'}), 401

        if admin.role != 2:
            return jsonify({'error': 'User is Unauthorized'}), 403

        user = get_user_by_id(user_id)
        if not user:
            return jsonify({'error': 'Invalid user id'}), 400

        updated_user = update_user(user.id, {'verified': verify})
        response_data = {
            'user_id': str(updated_user.id),
            'first_name': updated_user.first_name,
            'last_name': updated_user.last_name,
            'email': updated_user.email,
            'license_number': updated_user.license_number,
            'verified': updated_user.verified
        }

        return jsonify(response_data), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400