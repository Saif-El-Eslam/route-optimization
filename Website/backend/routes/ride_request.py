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
        # e. Update the User document
        updated_user = update_user(retrieved_user.id, {"ride_id": ride.id}) 
    
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

        route = bus.route
        route = route[1:-1]
        print("route: " + str(route))

        locations = bus.locations
        current_location = bus.current_location
        current_location = [float(i) for i in current_location]
        ordered_locations = []
        for i in route:
            ordered_locations.append(locations[i-1])
        print("ordered_locations: " + str(ordered_locations))
        current_location_entry = {"trip_id": "current_location", "action": "current_location", "coordinates": current_location}
        ordered_locations.insert(0, current_location_entry)
        distance, duration, path = calcluate_trip_parmaters([i["coordinates"] for i in ordered_locations])
        # send the response(distance, duration, path, ordered_locations)
        # convert object id to string
        for i in ordered_locations:
            i["trip_id"] = str(i["trip_id"])
            
        response_data = {
            "distance": distance,
            "duration": duration,
            "path": path,
            "locations": ordered_locations,
            'bus_id': bus.bus_id,
            'capacity': bus.capacity,
            'status': bus.status,
        }
        return jsonify(response_data)

    except Exception as e:
        return jsonify({'error': str(e)}), 400


@ride_request_bp.route("/update_current_location", methods=["POST"])
def update_location():
    
    bearer_token = request.headers.get('Authorization')
    token = bearer_token.split(' ')[1]
    try:
        user = get_user_by_token(token)
        if not user:
            return jsonify({'error': 'Invalid token'}), 401

        if user.role != 1:
            return jsonify({'error': 'User is Unauthorized'}), 403

        print("user.bus_id: " + str(user.bus_id))
        bus = get_bus_by_id(user.bus_id)
        if not bus:
            return jsonify({'error': 'Bus not found'}), 404

        data = request.get_json()
        location = data.get("location").get("coordinates")
        bus.current_location = location
        bus.save()
        
        locations_list = bus.locations
        current_location = bus.current_location
        next_location_index = bus.route[1]
        next_location = locations_list[next_location_index-1]
        distance,duration,path = get_distance_between_two_loc(current_location, next_location["coordinates"])
        print("distance: " + str(distance))
        if distance < 0.1:
            # remove the second location from the route
            bus.route.pop(1)
            #  drop next_location_index from the locations list
            bus.locations.pop(0)
            # update the locations list in the bus document
            bus.locations = bus.locations
            bus.save()
            # update the status of the ride to "Active"
            ride = get_ride_by_id(bus.assigned_trips[0])
            ride.status = "Active"
            ride.save()
        elif distance < 0.1:
            # remove the second location from the route
            bus.route.pop(1)
            # substact 1 from all the locations in the route for the next locations
            for i in range(1, len(bus.route)):
                if bus.route[i] > next_location_index:
                    bus.route[i] -= 1

            # TODO: update the time_window for the next locations
            #  drop next_location_index from the locations list
            bus.locations.pop(0)
            # update the locations list in the bus document
            bus.locations = bus.locations
            bus.save()
            # update the status of the ride to "Completed"
            ride = get_ride_by_id(bus.assigned_trips[0])
            ride.status = "Completed"
            ride.save()
            # remove the trip id from assigned_trips in the bus document
            bus.assigned_trips.remove(ride.id)
            bus.save()
        return jsonify({"message": "Current location updated"}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400
 
# get ride info for the rider
@ride_request_bp.route("/ride_info", methods=["GET"])
def get_ride_info():
    bearer_token = request.headers.get('Authorization')
    token = bearer_token.split(' ')[1]
    try:
        user = get_user_by_token(token)
        if not user:
            return jsonify({'error': 'Invalid token'}), 401
        if user.role != 0:
            return jsonify({'error': 'User is Unauthorized'}), 403
        

        ride = get_ride_by_id(user.ride_id)
        if not ride:
            return jsonify({'error': 'Ride not found'}), 404
        

        # distance_to_pickup, duration_to_pickup, path_to_pickup, distance_to_dropoff, duration_to_dropoff, path_to_dropoff = get_trip_updates(ride.id)
        # send the response(distance, duration, path, ordered_locations)
        # convert object id to string
        response_data = {
            "tripId": str(ride.id),
            "busId": ride.bus.bus_id,
            # "capacity": bus.capacity,
            "pickup_coordinates": ride.start_location,
            "dropoff_coordinates": ride.end_location,
            "status": ride.status,
            # "pickupTime": pickup_time,
            # "dropoffTime": dropoff_time,
            # "distanceToPickup": distance_to_pickup,
            # "timeToPickup": duration_to_pickup,
            # "pathToPickup": path_to_pickup,
            # "distanceToDropoff": distance_to_dropoff,
            # "timeToDropoff": duration_to_dropoff,
            # "pathToDropoff": path_to_dropoff
        }
        return jsonify(response_data)

    except Exception as e:
        return jsonify({'error': str(e)}), 400

# check bus arrival at pickup/dropoff location
# @ride_request_bp.route("/check_arrival", methods=["POST"])
# def check_arrival():
#     bearer_token = request.headers.get('Authorization')
#     token = bearer_token.split(' ')[1]
#     #1. check if the distance between the current location and the first location in the list is less than 0.1 miles
#     #2. if yes,
#         # if the action is pickup, update the status of the ride to "Active"
#         # if the action is dropoff, update the status of the ride to "Completed"
#         # remove the first location from the list
#         # update the locations list in the bus document
#     #3. if no, return the current location
#     try:
#         user = get_user_by_token(token)
#         if not user:
#             return jsonify({'error': 'Invalid token'}), 401

#         if user.role != 1:
#             return jsonify({'error': 'User is Unauthorized'}), 403

#         bus = get_bus_by_id(user.bus_id)
#         if not bus:
#             return jsonify({'error': 'Bus not found'}), 404

#         locations_list = bus.locations
#         current_location = bus.current_location
#         next_location_index = bus.route[1]
#         next_location = locations_list[next_location_index-1]
#         distance_to_next_location, duration_to_next_location, path_to_next_location = calcluate_trip_parmaters([current_location, next_location["coordinates"]])
#         if distance_to_next_location < 0.1:
#             # remove the second location from the route
#             bus.route.pop(1)
#             #  drop next_location_index from the locations list
#             locations_list.pop(next_location_index-1)
#             # update the locations list in the bus document
#             bus.locations = locations_list
            
#             bus.save()
#             # update the status of the ride to "Active" or "Completed"
#             if next_location["action"] == "pickup":
#                 ride = get_ride_by_id(next_location["trip_id"])
#                 ride.status = "Active"
#                 ride.save()
#             elif next_location["action"] == "dropoff":
#                 ride = get_ride_by_id(next_location["trip_id"])
#                 ride.status = "Completed"
#                 ride.save()
#                 # remove the trip id from assigned_trips in the bus document
#                 bus.assigned_trips.remove(ride.id)
#                 bus.save()
#             return jsonify({"message": "Bus arrived at pickup/dropoff location"}), 200
#         else:
#             return jsonify({"error": "Bus not at pickup/dropoff location"}), 400
        
#     except Exception as e:
#         return jsonify({'error': str(e)}), 400
    

        


def get_trip_updates(trip_id):
    # get trip (ride request) from db
    trip = get_ride_by_id(trip_id)
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
    # print("locations_list: " + str(locations_list))
    # get duration between stops
    max_locations_list = 25  # Maximum number of locations_list per API request
    num_requests = (len(locations_list) - 1) // (max_locations_list - 1) + 1  # Number of API requests needed
    distance=0
    duration=0
    path=[]
    # print("num_requests: " + str(num_requests))
    for req in range(num_requests):
        start = req * (max_locations_list - 1)
        end = min(start + max_locations_list, len(locations_list))
        # print("Trial one:", start, end)
        URL = 'https://api.mapbox.com/directions/v5/mapbox/driving/'
        for i in range(start, end ):
            URL += "{},{};".format(locations_list[i][0], locations_list[i][1])

        URL = URL[:-1]
        URL+="?alternatives=false&geometries=geojson&language=en&overview=full&steps=false&access_token=pk.eyJ1IjoiYWhtZWR5MTU1MjAwIiwiYSI6ImNsamw4cDM3NDAzejAzZG1uc2Y4MGJ4aWIifQ.9z0OvMdr2pISeiDFf4ufTw"
        # print("URL: " + str(URL))
        response = requests.get(URL)
    
        if response.status_code == 200:
            data = response.json()
            distance+=data['routes'][0]['distance']*0.000621371
            duration+=data['routes'][0]['duration']/60
            # Extract the geometry
            path_coordinates = data['routes'][0]['geometry']['coordinates']
            path.extend(path_coordinates)
    return distance,duration,path


def get_distance_between_two_loc(loc1, loc2):
    URL = 'https://api.mapbox.com/directions/v5/mapbox/driving/'
    URL += "{},{};{},".format(loc1[0], loc1[1], loc2[0], loc2[1])
    URL = URL[:-1]
    URL += "?alternatives=false&geometries=geojson&language=en&overview=full&steps=false&access_token=pk.eyJ1IjoiYWhtZWR5MTU1MjAwIiwiYSI6ImNsamw4cDM3NDAzejAzZG1uc2Y4MGJ4aWIifQ.9z0OvMdr2pISeiDFf4ufTw"

    response = requests.get(URL)

    distance = 0
    duration = 0
    path = []

    if response.status_code == 200:
        data = response.json()
        distance += data['routes'][0]['distance'] * 0.000621371
        duration += data['routes'][0]['duration'] / 60
        path_coordinates = data['routes'][0]['geometry']['coordinates']
        path.extend(path_coordinates)

    return distance, duration, path

if __name__ == "__main__":
    ride_request_bp.run(debug=True)
