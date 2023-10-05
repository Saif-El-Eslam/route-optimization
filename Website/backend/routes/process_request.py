from flask import Flask, request, jsonify
from datetime import datetime
from db_connection import db
from schemas import *
from services import *

app = Flask(__name__)

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

        # 1. add the request to the database (RideRequest document)
        created_ride_request = create_ride_request(
            {
                "rider_id": "Rider13",
                "request_time": request_time,
                "start_location": pickup_location,
                "end_location": dropoff_location,
                "status": "Pending",
            }
        )
        # print("Created Rider Request:", created_ride_request.rider_id)

        # 2. get all the buses and their current locations from the database (Bus document)
        buses = get_all_buses()
        # 3. find the best bus to assign to the request
        # data to send : [depot, list locations]
        # a.
        # b.
        # 4. assign the request to the bus (Trip document, Bus document)
        # 6. return the response to the client

        # Simulate processing by assigning a bus route and bus
        assigned_bus_route = "Route A"
        assigned_bus = bus_routes["Route A"][0]

        # Simulated drop-off time (add some logic here based on your requirements)
        dropoff_time = "12:00 PM"

        # Create the response JSON
        response_data = {
            "dropoff time": dropoff_time,
            "assigned bus": assigned_bus,
            "assigned bus route": assigned_bus_route,
        }

        return jsonify(response_data)

    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)
