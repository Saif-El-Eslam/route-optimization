from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
import pytz
import requests
from schemas import *
from services import *
from optimizer import find_best_bus
from bson import ObjectId

ride_request_bp = Blueprint("ride_request_bp", __name__)


@ride_request_bp.route("/ride_request", methods=["POST"])
def ride_request():
    try:
        # Get data from the JSON request
        data = request.get_json()
        # # Extract request details
        # request time is the current time
        request_time = datetime.now(pytz.timezone("America/New_York"))
        pickup_location = data.get("pickupLocation").get("coordinates")
        dropoff_location = data.get("dropoffLocation").get("coordinates")
        passenger_count = data.get("passengerCount")
        user_token = data.get("userToken")
        # 1. add the request to the database (RideRequest document)
        retrieved_user = get_user_by_token(user_token)

        rider_data = {
            "rider": retrieved_user,
            "request_time": request_time,
            "start_location": pickup_location,  # [longitude, latitude]
            "end_location": dropoff_location,  # [longitude, latitude]
            "status": "Pending",
            "bus": ObjectId(),
            "pickup_time": "2021-03-01 12:00:00",
            "dropoff_time": "2021-03-01 12:00:00",
        }
        print(rider_data)
        ride = create_ride(rider_data)
        buses = get_all_buses()
        # 2. find the best bus to assign to the ride
        # a. get all the buses and their current locations from the database (Bus document)
        # b. find the best bus to assign to the ride (best_bus = find_best_bus(buses, ride))
        best_bus = find_best_bus(buses, ride)
        if best_bus is None:
            print("No bus available for ride " + str(ride.id))
            return jsonify({"error": "No bus available"}), 400
        # c. Update the Bus document
        updated_bus = update_bus(best_bus.bus_id, best_bus.to_mongo())
        print("updated_bus: " + str(updated_bus))
        updated_ride = update_ride(ride.id, {
            "status": "Assigned", "bus": best_bus})
        # d. Update the RideRequest document
        distance_to_pickup, duration_to_pickup, path_to_pickup, distance_to_dropoff, duration_to_dropoff, path_to_dropoff = get_trip_updates(ride.id)
        pickup_time = request_time + timedelta(minutes=duration_to_pickup)
        dropoff_time = pickup_time + timedelta(minutes=duration_to_dropoff)
        print("pickup_time: " + str(pickup_time))
        print("dropoff_time: " + str(dropoff_time))
        updated_ride = update_ride(ride.id, {
             "pickup_time": pickup_time, "dropoff_time": dropoff_time})

        # Create the response JSON
        response_data = {
            "tripId": str(updated_ride.id),
            "busId": updated_bus.bus_id,
            "pickupTime": pickup_time,
            "dropoffTime": dropoff_time,
            "distanceToPickup": distance_to_pickup,
            "durationToPickup": duration_to_pickup,
            "pathToPickup": path_to_pickup,
            "distanceToDropoff": distance_to_dropoff,
            "durationToDropoff": duration_to_dropoff,
            "pathToDropoff": path_to_dropoff
        }

        return jsonify(response_data)

    except Exception as e:
        return jsonify({"error": str(e)}), 400

@ride_request_bp.route("/bus_route", methods=["GET"])
def get_bus_route():
    data = request.get_json()
    bus_id = data.get("busId")
    bus = get_bus_by_id(bus_id)
    route = bus.route
    route = route[1:-1]

    locations = bus.locations
    current_location = bus.current_location
    current_location = [float(i) for i in current_location]
    ordered_locations = []
    for i in route:
        ordered_locations.append(locations[i-1])
    current_location_entry = {"trip_id": "current_location", "action": "current_location", "coordinates": current_location}
    ordered_locations.insert(0, current_location_entry)
    distance, duration, path = calcluate_trip_parmaters([i["coordinates"] for i in ordered_locations])
    response_data = {
        "distance": distance,
        "duration": duration,
        "path": path,
        "locations": ordered_locations
    }

    return jsonify(response_data)

# @ride_request_bp.route("/get_updates", methods=["GET"])
# def get_trip_updates():
#     # get user id , trip id from the body
#     data = request.get_json()
#     trip_id = data.get("tripId")
#     distance_to_pickup, duration_to_pickup, path_to_pickup = get_trip_updates(trip_id)
#     distance_to_dropoff, duration_to_dropoff, path_to_dropoff = get_trip_updates(trip_id)
    
#     response_data = {
#         "distanceToPickup": distance_to_pickup,
#         "durationToPickup": duration_to_pickup,
#         "pathToPickup": path_to_pickup,
#         "distanceToDropoff": distance_to_dropoff,
#         "durationToDropoff": duration_to_dropoff,
#         "pathToDropoff": path_to_dropoff
#     }
#     #TODO: update the ride in the database
#     return jsonify(response_data)



def get_trip_updates(trip_id):
    # get trip (ride request) from db
    trip = get_ride(trip_id)
    print("trip: " + str(trip))
    #  get bus from trip
    # trip.bus is a reference field (ObjectId) to the bus document
    bus = get_bus_by_id(trip.bus.bus_id)
    # get route from bus
    route = bus.route
    # remove first and last locations from route
    route = route[1:-1]
    print("route: " + str(route))
    
    # get locations from bus
    locations = bus.locations
    print("locations: " + str(locations))
    # get current location from bus
    current_location = bus.current_location
    # convert current location to float
    current_location = [float(i) for i in current_location]
    print("current_location: " + str(current_location))
    # arrange locations in the order of the route
    ordered_locations = []
    for i in route:
        ordered_locations.append(locations[i-1])
    # append current location to the beginning of the list
    current_location_entry = {"trip_id": trip.id, "action": "current_location", "coordinates": current_location}
    ordered_locations.insert(0, current_location_entry)
    print("ordered_locations: " + str(ordered_locations))
    # get list of locations from current location to pickup location
    pickup_location = {"trip_id": trip.id, "action": "pickup", "coordinates": [float(i) for i in trip.start_location]}
    locations_to_pickup = ordered_locations[0:ordered_locations.index(pickup_location)+1]
    print("locations_to_pickup: " + str(locations_to_pickup))
    # get list of locations from pickup location to dropoff location
    dropoff_location = {"trip_id": trip.id, "action": "dropoff", "coordinates": [float(i) for i in trip.end_location]}
    locations_to_dropoff = ordered_locations[ordered_locations.index(pickup_location):ordered_locations.index(dropoff_location)+1]
    print("locations_to_dropoff: " + str(locations_to_dropoff))
    distance_to_pickup, duration_to_pickup, path_to_pickup = calcluate_trip_parmaters([i["coordinates"] for i in locations_to_pickup])
    distance_to_dropoff, duration_to_dropoff, path_to_dropoff = calcluate_trip_parmaters([i["coordinates"] for i in locations_to_dropoff])

    return distance_to_pickup, duration_to_pickup, path_to_pickup, distance_to_dropoff, duration_to_dropoff, path_to_dropoff

def calcluate_trip_parmaters(locations_list):
    MAPBOX_TOKEN="pk.eyJ1IjoiYWhtZWR5MTU1MjAwIiwiYSI6ImNsamw4cDM3NDAzejAzZG1uc2Y4MGJ4aWIifQ.9z0OvMdr2pISeiDFf4ufTw"
    print("locations_list: " + str(locations_list))
    # get duration between stops
    max_locations_list = 25  # Maximum number of locations_list per API request
    num_requests = (len(locations_list) - 1) // (max_locations_list - 1) + 1  # Number of API requests needed
    distance=0
    duration=0
    path=[]
    print("num_requests: " + str(num_requests))
    for req in range(num_requests):
        start = req * (max_locations_list - 1)
        end = min(start + max_locations_list, len(locations_list))
        # print("Trial one:", start, end)
        URL = 'https://api.mapbox.com/directions/v5/mapbox/driving/'
        for i in range(start, end ):
            URL += "{},{};".format(locations_list[i][0], locations_list[i][1])

        URL = URL[:-1]
        URL+="?alternatives=false&geometries=geojson&language=en&overview=full&steps=false&access_token=pk.eyJ1IjoiYWhtZWR5MTU1MjAwIiwiYSI6ImNsamw4cDM3NDAzejAzZG1uc2Y4MGJ4aWIifQ.9z0OvMdr2pISeiDFf4ufTw"
        print("URL: " + str(URL))
        response = requests.get(URL)
    
        if response.status_code == 200:
            data = response.json()
            distance+=data['routes'][0]['distance']*0.000621371
            duration+=data['routes'][0]['duration']/60
            # Extract the geometry
            path_coordinates = data['routes'][0]['geometry']['coordinates']
            path.extend(path_coordinates)
    return distance,duration,path

if __name__ == "__main__":
    ride_request_bp.run(debug=True)
