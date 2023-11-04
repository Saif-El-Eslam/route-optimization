from flask import Blueprint, request, jsonify
from flask_cors import CORS

from services import *
from schemas import *
from auth_handlers import get_user_by_token

driver_requests_bp = Blueprint('driver_requests_bp', __name__)

@driver_requests_bp.route('/my-bus', methods=['GET'])
def get_bus():
    bearer_token = request.headers.get('Authorization')
    token = bearer_token.split(' ')[1]

    try:
        user = get_user_by_token(token)
        if not user:
            return jsonify({'error': 'Invalid token'}), 401

        if user.role != 1:
            return jsonify({'error': 'Unauthorized'}), 403

        bus = get_bus_by_id(user.bus_id)
        if not bus:
            return jsonify({'error': 'Bus not found'}), 404

        response_data = {
            'bus_id': bus.bus_id,
            'capacity': bus.capacity,
            'current_location': bus.current_location,
            'locations': bus.locations,
            'route': bus.route,
            'time_windows': bus.time_windows,
            'assigned_trips': bus.assigned_trips,
            'status': bus.status,
            'depot': bus.depot,
        }

        return jsonify(response_data), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400

@driver_requests_bp.route('/verify-bus', methods=['POST'])
def verify_bus():
    bearer_token = request.headers.get('Authorization')
    token = bearer_token.split(' ')[1]

    data = request.get_json()
    verify = data.get('verify')

    try:
        user = get_user_by_token(token)
        if not user:
            return jsonify({'error': 'Invalid token'}), 401

        if user.role != 1:
            return jsonify({'error': 'Unauthorized'}), 403
        
        updated_bus = update_bus(user.bus_id, {'status': verify})
        response_data = {
            'bus_id': updated_bus.bus_id,
            'capacity': updated_bus.capacity,
            'current_location': updated_bus.current_location,
            'locations': updated_bus.locations,
            'route': updated_bus.route,
            'time_windows': updated_bus.time_windows,
            'assigned_trips': updated_bus.assigned_trips,
            'status': updated_bus.status,
            'depot': updated_bus.depot,
        }

        return jsonify(response_data), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400