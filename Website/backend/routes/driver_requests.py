from flask import Blueprint, request, jsonify
from flask_cors import CORS

from services import *
from schemas import *
from auth_handlers import get_user_by_token
from bson import ObjectId
import json

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
            return jsonify({'error': 'User is Unauthorized'}), 403

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
            return jsonify({'error': 'User is Unauthorized'}), 403
        updated_bus = update_bus(user.bus_id, {'status': verify})
        response_data = {
            'status': updated_bus.status,
        }

        return jsonify(response_data), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400


@driver_requests_bp.route('/customer_name/<trip_id>', methods=['GET'])
def get_customer_name(trip_id):
    try:
        trip = get_ride_by_id(ObjectId(trip_id))
        
        # trip.rider is a user object, convert it to json then to a dictionary
        dictTripRider = json.loads(trip.rider.to_json())
        # get the user id from the dictionary
        userId = dictTripRider["_id"]["$oid"]


        if not trip:
            return jsonify({'error': 'Trip not found'}), 404

        user = get_user_by_id(ObjectId(userId))

        if not user:
            return jsonify({'error': 'User not found'}), 404

        response_data = {
            'name': user.first_name + " " + user.last_name,
        }

        return jsonify(response_data), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400