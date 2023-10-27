from flask import Blueprint, request, jsonify
from flask_cors import CORS
from datetime import datetime
from schemas import *
from services import *

app = Flask(__name__)
CORS(app, supports_credentials=True)
process_request_bp = Blueprint("process_request_bp", __name__)

# Simulated data for bus routes and buses
bus_routes = {
    "Route A": ["Bus 101", "Bus 102"],
    "Route B": ["Bus 201", "Bus 202"],
}


# Define a route to handle incoming requests


@app.route("/process_request", methods=["POST"])
def process_request():
    try:
        # Get data from the JSON request
        data = request.get_json()

        # Extract request details
        request_time = data.get("requestTime")
        pickup_location = data.get("pickupLocation")
        dropoff_location = data.get("dropoffLocation")
        passenger_count = data.get("passengerCount")
        rider_id = data.get("riderId")

        # 1. add the request to the database (RideRequest document)
        created_ride_request = create_ride_request(
            {
                "rider_id": rider_id,
                "request_time": request_time,
                "start_location": pickup_location,
                "end_location": dropoff_location,
                "status": "Pending",
            }
        )

        created_trip = create_trip({
            "bus_id": "",
            "rider_id": rider_id,
            "request_time": request_time,
            "pickup_time": "",
            "arrival_time": "",
            "pickup_location": pickup_location,
            "dropoff_location": dropoff_location,
            "status": "Pending"})

        # TODO: get all ride requests and loop over them executing the following steps:
        requests = get_ride_requests_by_status("Pending")
        for request in requests:
            # 2. find the best bus to assign to the request
            # a. get all the buses and their current locations from the database (Bus document)
            buses = get_all_buses()
            # b. find the best bus to assign to the request
            # test(buses, request)

        # Simulate processing by assigning a bus route and bus
        assigned_bus_route = "Route A"
        assigned_bus = bus_routes["Route A"][0]

        # Simulated drop-off time (add some logic here based on your requirements)
        pickup_time = "12:00 PM"
        dropoff_time = "12:00 PM"

        # Create the response JSON
        response_data = {
            "pickup time": pickup_time,
            "dropoff time": dropoff_time,
            "assigned bus": assigned_bus,
            "assigned bus route": assigned_bus_route,
        }

        return jsonify(response_data)

    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)
