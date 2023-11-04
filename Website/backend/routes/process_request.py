from flask import Blueprint, request, jsonify
from datetime import datetime
from schemas import *
from services import *
from optimizer import find_best_bus
from bson import ObjectId

process_request_bp = Blueprint("process_request_bp", __name__)

@process_request_bp.route("/process_request", methods=["POST"])
def process_request():
    try:
        # Get data from the JSON request
        data = request.get_json()
        # # Extract request details
        request_time = data.get("requestTime")
        pickup_location = data.get("pickupLocation")
        dropoff_location = data.get("dropoffLocation")
        passenger_count = data.get("passengerCount")
        user_token = data.get("userToken")

        # 1. add the request to the database (RideRequest document)
        retrieved_user = get_user_by_token(user_token)
        
        rider_request_data = {
        "rider": retrieved_user,
        "request_time": "2021-03-01 12:00:00",
        "start_location": [-85.617046, 42.3030528],  # [longitude, latitude
        "end_location": [-85.617046, 42.3030528],  # [longitude, latitude]
        "status": "Pending",
        "bus": ObjectId(),
        "pickup_time": "2021-03-01 12:00:00",
        "dropoff_time": "2021-03-01 12:00:00",
        }
        ride_request = create_ride(rider_request_data)
        buses = get_all_buses()
        # 2. find the best bus to assign to the ride_request
        # a. get all the buses and their current locations from the database (Bus document)
        # b. find the best bus to assign to the ride_request (best_bus = find_best_bus(buses, ride_request))
        best_bus = find_best_bus(buses, ride_request)
        if best_bus is None:
            print("No bus available for ride_request " + str(ride_request.id))
            return jsonify({"error": "No bus available"}), 400
        # c. Update the Bus document
        updated_bus = update_bus(best_bus.bus_id, best_bus.to_mongo())
        # d. Update the RideRequest document
        # pickup_time, dropoff_time = get_pickup_dropoff_times(
        #     request.id, request.request_time, best_bus.current_location, best_bus.locations, best_bus.route)
        pickup_time = "2021-03-01 12:00:00"
        dropoff_time = "2021-03-01 12:00:00"
        updated_ride = update_ride(ride_request.id, {
                                                "status": "Assigned", "bus": best_bus, "pickup_time": pickup_time, "dropoff_time": dropoff_time})
        
        # Create the response JSON
        response_data = {
            "tripId": str(updated_ride.id),
            "busId": updated_bus.bus_id,
            "pickupTime": pickup_time,
            "dropoffTime": dropoff_time
        }
        
        return jsonify(response_data)

    except Exception as e:
        return jsonify({"error": str(e)}), 400

@process_request_bp.route("/get_updates", methods=["GET"])
def get_trip_updates():
    # get user id , trip id from the body
    data= request.get_json()
    trip_id = data.get("tripId")
    # get the path from the trip id
    path = get_trip_updates(trip_id)
    # return the path
    return jsonify(path) #FIXME: return all the data needed to update the map 


def get_trip_updates(trip_id):
    # get trip (ride request) from db
    trip = get_ride(trip_id)
    # get bus from db
    bus = get_bus(trip.bus_id)
    # get route from bus
    route = bus.route
    # get locations from bus
    locations = bus.locations
    # get current location from bus
    current_location = bus.current_location
    # get pickup location from trip
    pickup_location = trip.pickup_location
    # get dropoff location from trip
    dropoff_location = trip.dropoff_location
    # get the index of the pickup location in the route
    pickup_location_index = route.index(pickup_location)
    # get the index of the dropoff location in the route
    dropoff_location_index = route.index(dropoff_location)
    # get the index of the current location in the route
    current_location_index = route.index(current_location)
    # get the locations between the current location and the pickup location
    locations_before_pickup = locations[current_location_index:pickup_location_index]
    # get the locations between the pickup location and the dropoff location
    locations_after_pickup = locations[pickup_location_index:dropoff_location_index]
    # get the locations after the dropoff location
    locations_after_dropoff = locations[dropoff_location_index:]
    # get the locations before the current location
    locations_before_current = locations[:current_location_index]
    # reverse the locations before the current location
    locations_before_current.reverse()
    # create the path
    path = locations_before_current + locations_before_pickup + [pickup_location] + locations_after_pickup + [dropoff_location] + locations_after_dropoff
    return path #FIXME: return all the data needed to update the map. check the bus db(bus_id=5) for more info



if __name__ == "__main__":
    process_request_bp.run(debug=True)
