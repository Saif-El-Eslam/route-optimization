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
        # print(rider_data)
        ride = create_ride(rider_data)
        buses = get_all_buses()
        # 2. find the best bus to assign to the ride
        # a. get all the buses and their current locations from the database (Bus document)
        # b. find the best bus to assign to the ride (best_bus = find_best_bus(buses, ride))
        print("buses: " + str(buses))
        try:
            best_bus = find_best_bus(buses, ride)
        except Exception as e:
            delete_ride(ride.id)
            return jsonify({"error": str(e)}), 400

        if best_bus is None:
            # delete the ride request from the database
            delete_ride(ride.id)
            return jsonify({"error": "No bus available"}), 400

        # c. Update the Bus document
        updated_bus = update_bus(best_bus.bus_id, best_bus.to_mongo())
        # print("updated_bus: " + str(updated_bus))
        updated_ride = update_ride(ride.id, {
            "status": "Assigned", "bus": best_bus})
        # d. Update the RideRequest document
        distance_to_pickup, duration_to_pickup, path_to_pickup, distance_to_dropoff, duration_to_dropoff, path_to_dropoff = get_trip_updates(
            ride.id)
        pickup_time = request_time + timedelta(minutes=duration_to_pickup)
        dropoff_time = pickup_time + timedelta(minutes=duration_to_dropoff)
        # print("pickup_time: " + str(pickup_time))
        # print("dropoff_time: " + str(dropoff_time))
        updated_ride = update_ride(ride.id, {
            "pickup_time": pickup_time, "dropoff_time": dropoff_time})
        # e. Update the User document
        updated_user = update_user(
            retrieved_user.id, {"ride_id": str(ride.id)})

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
        # print("route: " + str(route))

        locations = bus.locations
        if len(locations) == 0:
            return jsonify(
                {"distance": 0,
                 "duration": 0,
                 "path": [],
                 "locations": [],
                 'bus_id': bus.bus_id,
                 'capacity': bus.capacity,
                 'status': bus.status,
                 }), 200

        current_location = bus.current_location
        current_location = [float(i) for i in current_location]
        ordered_locations = []
        for i in route:
            ordered_locations.append(locations[i-1])
        # print("ordered_locations: " + str(ordered_locations))
        current_location_entry = {"trip_id": "current_location",
                                  "action": "current_location", "coordinates": current_location}
        ordered_locations.insert(0, current_location_entry)
        distance, duration, path = calcluate_trip_parmaters(
            [i["coordinates"] for i in ordered_locations])
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
    """Update the current location of the bus 
    used by the driver to update the current location of the bus"""
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

        data = request.get_json()
        location = data.get("location").get("coordinates")
        bus.current_location = location
        bus.save()
        # if locations_list is empty, return
        if len(bus.locations) == 0:
            return jsonify({"message": "Current location updated"}), 200

        # Append the current location to the beginning of the locations list
        current_location_entry = {"trip_id": "current_location",
                                  "action": "current_location", "coordinates": location}
        bus.locations.insert(0, current_location_entry)
        # print("locations_list: " + str(bus.locations))
        current_location = bus.current_location
        # print("current_location: " + str(current_location))
        # the true index of the next location in the locations list
        next_location_index = bus.route[1]
        # print("next_location_index: " + str(next_location_index))
        next_location = bus.locations[next_location_index]
        # print("next_location: " +
        #       str(next_location["coordinates"]), "action: " + str(next_location["action"]))
        distance, _, _ = get_distance_between_two_loc(
            current_location, next_location["coordinates"])
        print("distance between", current_location, "and",
              next_location["coordinates"], "is", distance)
        # TODO: change it to while loop
        while distance < 0.02:  # 20 meters
            print("next_location_index (inside while loop): " +
                  str(next_location_index))
            
            # route:
            # remove the second location from the route
            print("route before: " + str(bus.route))
            # print("locations_list before: " + str(bus.locations))
            # print("time_windows before: " + str(bus.time_windows))
            # print("demands before: " + str(bus.demands))
            # print("pickups_deliveries before: " + str(bus.pickups_deliveries))

            bus.route.pop(1)
            # update the numbers in the route list (decrement by 1) as we removed the next location from the locations list
            for i in range(len(bus.route)):
                if bus.route[i] > next_location_index:
                    bus.route[i] -= 1
            print("route after: " + str(bus.route))

            # locations:
            # drop next_location_index from the locations list
            # -1 because the locations list in the bus doc does not contain the current location
            bus.locations.pop(next_location_index)
            # print("locations_list after: " + str(bus.locations))
            # time_windows:
            # drop next_location_index from the time_windows list
            # no -1 because the time_windows list contains the current location as the first element
            bus.time_windows.pop(next_location_index)
            # print("time_windows after: " + str(bus.time_windows))
            # demands list:
            # if the next location is a pickup location,
            # increment the first element in the demands list and remove the next location from the demands list

            if next_location["action"] == "pickup":
                bus.demands[0] += 1
                bus.demands.pop(next_location_index)
            # if the next location is a dropoff location,
            # decrement the first element in the demands list and remove the next location from the demands list
            elif next_location["action"] == "dropoff":
                bus.demands[0] -= 1
                bus.demands.pop(next_location_index)

            # pickups_deliveries:
            # if the next location is a pickup location,
            #  remove the list that contains the next location from the pickups_deliveries list
            if next_location["action"] == "pickup":
                for i in range(len(bus.pickups_deliveries)):
                    if next_location_index in bus.pickups_deliveries[i]:
                        # if it is the last element in the list, make any empty list [[]]
                        if len(bus.pickups_deliveries) == 1:
                            bus.pickups_deliveries = []
                        else:
                            bus.pickups_deliveries.pop(i)
                        break
            elif next_location["action"] == "dropoff":
                # if the next location is a dropoff location,
                #  remove the list that contains the next location from the pickup_deliveries list
                for i in range(len(bus.pickups_deliveries)):
                    if next_location_index in bus.pickups_deliveries[i]:
                        # if it is the last element in the list, make any empty list [[]]
                        if len(bus.pickups_deliveries) == 1:
                            bus.pickups_deliveries = []
                        else:
                            bus.pickups_deliveries.pop(i)
                        break
            # print("demands after: " + str(bus.demands))
            # update the numbers in the pickups_deliveries list (decrement by 1) as we removed the next location from the locations list
            # ex: [[1,2], [3,4], [5,6]] -> [[1,2], [3,4]]
            # print("Length of pickups_deliveries: " +
                #   str(len(bus.pickups_deliveries)))
            for i in range(len(bus.pickups_deliveries)):
                for j in range(len(bus.pickups_deliveries[i])):
                    if bus.pickups_deliveries[i][j] > next_location_index:
                        bus.pickups_deliveries[i][j] -= 1
            # print("pickups_deliveries after: " + str(bus.pickups_deliveries))
            # print("-------------------next location-------------------", next_location)
            # update the status of the ride to "Active" or "Completed"
            if next_location["action"] == "pickup":
                ride = get_ride_by_id(next_location["trip_id"])
                ride.status = "Active"
                # update the pickup time
                ride.pickup_time = datetime.now(
                    pytz.timezone("America/New_York"))

                ride.save()
            elif next_location["action"] == "dropoff":
                ride = get_ride_by_id(next_location["trip_id"])
                ride.status = "Completed"
                # update the dropoff time
                ride.dropoff_time = datetime.now(
                    pytz.timezone("America/New_York"))
                # remove the ride_id from the user document
                update_user(ride.rider.id, {"ride_id": ""})
                # remove the trip id from assigned_trips in the bus document
                bus.assigned_trips.remove(ride.id)

            ride.save()
            # update the bus document
            # pop the first element from the locations list (current location) for the optimizer to work correctly
            # if it is the last element in the list, make any empty list []
            print("locations_list after: " + str(bus.locations))
            if len(bus.locations) == 1:
                bus.locations = []
                bus.save()
                return jsonify({"message": "Current location updated"}), 200
            else:
                next_location_index = bus.route[1]
                next_location = bus.locations[next_location_index]
                distance, _, _ = get_distance_between_two_loc(
                    current_location, next_location["coordinates"])
                print("new distance between", current_location, "and",
                        next_location["coordinates"], "is", distance)
        bus.locations.pop(0)
        bus.save()
        return jsonify({"message": "Current location updated"}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400


# get ride info for the rider
@ride_request_bp.route("/ride_info", methods=["GET"])
def get_ride_info():
    """Get ride info for the rider"""
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

        distance_to_pickup, duration_to_pickup, path_to_pickup, distance_to_dropoff, duration_to_dropoff, path_to_dropoff = get_trip_updates(
            ride.id)
        response_data = {
            "tripId": str(ride.id),
            "busId": ride.bus.bus_id,
            # "capacity": bus.capacity, # Not Now
            "pickup_coordinates": ride.start_location,
            "dropoff_coordinates": ride.end_location,
            "status": ride.status,
            "distanceToPickup": distance_to_pickup,
            "timeToPickup": duration_to_pickup,
            "pathToPickup": path_to_pickup,
            "distanceToDropoff": distance_to_dropoff,
            "timeToDropoff": duration_to_dropoff,
            "pathToDropoff": path_to_dropoff
        }
        return jsonify(response_data)

    except Exception as e:
        return jsonify({'error': str(e)}), 400

@ride_request_bp.route("/restart_db", methods=["GET"])
def restart_db():
    """Restart the database"""
    for bus in Bus.objects:
        bus.delete()
    print("Deleted all buses")
    # Delete all rides
    for ride in Ride.objects:
        ride.delete()
    # Make the ride_id for all users of type rider "None"
    for user in User.objects(role=0):
        user.ride_id = ""
        user.save() 
    print("Deleted all rides")
    buses = [{'bus_id': '1', 'capacity': 24, 'current_location': [-85.5473919, 42.3226625], 'locations': [], 'route': [], 'time_windows': [[0, 1440]], 'assigned_trips': [], 'status': 'Active', 'depot': [-85.5473919, 42.3226625], 'pickups_deliveries': [], 'demands': [0]}, {'bus_id': '2', 'capacity': 24, 'current_location': [-85.6880877, 42.2666994], 'locations': [], 'route': [], 'time_windows': [[0, 1440]], 'assigned_trips': [], 'status': 'Active', 'depot': [-85.6880877, 42.2666994], 'pickups_deliveries': [], 'demands': [0]}, {'bus_id': '3', 'capacity': 24, 'current_location': [-85.5624162, 42.2977748], 'locations': [], 'route': [], 'time_windows': [[0, 1440]], 'assigned_trips': [], 'status': 'Active', 'depot': [-85.5624162, 42.2977748], 'pickups_deliveries': [], 'demands': [0]}, {'bus_id': '4', 'capacity': 24, 'current_location': [-85.5940978, 42.2470918], 'locations': [], 'route': [], 'time_windows': [[0, 1440]], 'assigned_trips': [], 'status': 'Active', 'depot': [-85.5940978, 42.2470918], 'pickups_deliveries': [], 'demands': [0]}, {'bus_id': '5', 'capacity': 24, 'current_location': [-85.6102235, 42.2845248], 'locations': [], 'route': [], 'time_windows': [[0, 1440]], 'assigned_trips': [], 'status': 'Active', 'depot': [-85.6102235, 42.2845248], 'pickups_deliveries': [], 'demands': [0]}, {'bus_id': '6', 'capacity': 24, 'current_location': [-85.5355127, 42.334607], 'locations': [], 'route': [], 'time_windows': [[0, 1440]], 'assigned_trips': [], 'status': 'Active', 'depot': [-85.5355127, 42.334607], 'pickups_deliveries': [], 'demands': [0]}, {'bus_id': '7', 'capacity': 24, 'current_location': [-85.5945787, 42.2475577], 'locations': [], 'route': [], 'time_windows': [[0, 1440]], 'assigned_trips': [], 'status': 'Active', 'depot': [-85.5945787, 42.2475577], 'pickups_deliveries': [], 'demands': [0]}, {'bus_id': '8', 'capacity': 24, 'current_location': [-85.5544953, 42.2991703], 'locations': [], 'route': [], 'time_windows': [[0, 1440]], 'assigned_trips': [], 'status': 'Active', 'depot': [-85.5544953, 42.2991703], 'pickups_deliveries': [], 'demands': [0]}, {'bus_id': '9', 'capacity': 24, 'current_location': [-85.5636076, 42.2513353], 'locations': [], 'route': [], 'time_windows': [[0, 1440]], 'assigned_trips': [], 'status': 'Active', 'depot': [-85.5636076, 42.2513353], 'pickups_deliveries': [], 'demands': [0]}, {'bus_id': '10', 'capacity': 24, 'current_location': [-85.6087517, 42.2077529], 'locations': [], 'route': [], 'time_windows': [[0, 1440]], 'assigned_trips': [], 'status': 'Active', 'depot': [-85.6087517, 42.2077529], 'pickups_deliveries': [], 'demands': [0]}, {'bus_id': '11', 'capacity': 24, 'current_location': [-85.457795, 42.399715], 'locations': [], 'route': [], 'time_windows': [[0, 1440]], 'assigned_trips': [], 'status': 'Active', 'depot': [-85.457795, 42.399715], 'pickups_deliveries': [], 'demands': [0]}, {'bus_id': '12', 'capacity': 24, 'current_location': [-85.4727853, 42.1543539], 'locations': [], 'route': [], 'time_windows': [[0, 1440]], 'assigned_trips': [], 'status': 'Active', 'depot': [-85.4727853, 42.1543539], 'pickups_deliveries': [], 'demands': [0]}, {'bus_id': '13', 'capacity': 24, 'current_location': [-85.5550967, 42.2581612], 'locations': [], 'route': [], 'time_windows': [[0, 1440]], 'assigned_trips': [], 'status': 'Active', 'depot': [-85.5550967, 42.2581612], 'pickups_deliveries': [], 'demands': [0]}, {'bus_id': '14', 'capacity': 24, 'current_location': [-85.6320449, 42.2964597], 'locations': [], 'route': [], 'time_windows': [[0, 1440]], 'assigned_trips': [], 'status': 'Active', 'depot': [-85.6320449, 42.2964597], 'pickups_deliveries': [], 'demands': [0]}, {'bus_id': '15', 'capacity': 24, 'current_location': [-85.4683159, 42.3747781], 'locations': [], 'route': [], 'time_windows': [[0, 1440]], 'assigned_trips': [], 'status': 'Active', 'depot': [-85.4683159, 42.3747781], 'pickups_deliveries': [], 'demands': [0]}, {'bus_id': '16', 'capacity': 24, 'current_location': [-85.5859105, 42.2829969], 'locations': [], 'route': [], 'time_windows': [[0, 1440]], 'assigned_trips': [], 'status': 'Active', 'depot': [-85.5859105, 42.2829969], 'pickups_deliveries': [], 'demands': [0]}, {'bus_id': '17', 'capacity': 24, 'current_location': [-85.409809, 42.2933292], 'locations': [], 'route': [], 'time_windows': [[0, 1440]], 'assigned_trips': [], 'status': 'Active', 'depot': [-85.409809, 42.2933292], 'pickups_deliveries': [], 'demands': [0]}, {'bus_id': '18', 'capacity': 24, 'current_location': [-85.5033838, 42.1410135], 'locations': [], 'route': [], 'time_windows': [[0, 1440]], 'assigned_trips': [], 'status': 'Active', 'depot': [-85.5033838, 42.1410135], 'pickups_deliveries': [], 'demands': [0]}, {'bus_id': '19', 'capacity': 24, 'current_location': [-85.5221051, 42.3280919], 'locations': [], 'route': [], 'time_windows': [[0, 1440]], 'assigned_trips': [], 'status': 'Active', 'depot': [-85.5221051, 42.3280919], 'pickups_deliveries': [], 'demands': [0]}, {'bus_id': '20', 'capacity': 24, 'current_location': [-85.5844838, 42.1729487], 'locations': [], 'route': [], 'time_windows': [[0, 1440]], 'assigned_trips': [], 'status': 'Active', 'depot': [-85.5844838, 42.1729487], 'pickups_deliveries': [], 'demands': [0]}, {'bus_id': '21', 'capacity': 24, 'current_location': [-85.7262985, 42.2457494], 'locations': [], 'route': [], 'time_windows': [[0, 1440]], 'assigned_trips': [], 'status': 'Active', 'depot': [-85.7262985, 42.2457494], 'pickups_deliveries': [], 'demands': [0]}, {'bus_id': '22', 'capacity': 24, 'current_location': [-85.5794339, 42.262203], 'locations': [], 'route': [], 'time_windows': [[0, 1440]], 'assigned_trips': [], 'status': 'Active', 'depot': [-85.5794339, 42.262203], 'pickups_deliveries': [], 'demands': [0]}, {'bus_id': '23', 'capacity': 24, 'current_location': [-85.5316711, 42.3407718], 'locations': [], 'route': [], 'time_windows': [[0, 1440]], 'assigned_trips': [], 'status': 'Active', 'depot': [-85.5316711, 42.3407718], 'pickups_deliveries': [], 'demands': [0]}, {'bus_id': '24', 'capacity': 24, 'current_location': [-85.7507622, 42.2836978], 'locations': [], 'route': [], 'time_windows': [[0, 1440]], 'assigned_trips': [], 'status': 'Active', 'depot': [-85.7507622, 42.2836978], 'pickups_deliveries': [], 'demands': [0]}, {'bus_id': '25', 'capacity': 24, 'current_location': [-85.5585162, 42.3321206], 'locations': [], 'route': [], 'time_windows': [[0, 1440]], 'assigned_trips': [], 'status': 'Active', 'depot': [-85.5585162, 42.3321206], 'pickups_deliveries': [], 'demands': [0]}, {'bus_id': '26', 'capacity': 24, 'current_location': [-85.6114028, 42.2036211], 'locations': [], 'route': [], 'time_windows': [[0, 1440]], 'assigned_trips': [], 'status': 'Active', 'depot': [-85.6114028, 42.2036211], 'pickups_deliveries': [], 'demands': [0]}, {'bus_id': '27', 'capacity': 24, 'current_location': [-85.7507622, 42.2836978], 'locations': [], 'route': [], 'time_windows': [[0, 1440]], 'assigned_trips': [], 'status': 'Active', 'depot': [-85.7507622, 42.2836978], 'pickups_deliveries': [], 'demands': [0]}, {'bus_id': '28', 'capacity': 24, 'current_location': [-85.5701549, 42.2196805], 'locations': [], 'route': [], 'time_windows': [[0, 1440]], 'assigned_trips': [], 'status': 'Active', 'depot': [-85.5701549, 42.2196805], 'pickups_deliveries': [], 'demands': [0]}, {'bus_id': '29', 'capacity': 24, 'current_location': [-85.4735514, 42.3071286], 'locations': [], 'route': [], 'time_windows': [[0, 1440]], 'assigned_trips': [], 'status': 'Active', 'depot': [-85.4735514, 42.3071286], 'pickups_deliveries': [], 'demands': [0]}, {'bus_id': '30', 'capacity': 24, 'current_location': [-85.642907, 42.2749172], 'locations': [], 'route': [], 'time_windows': [[0, 1440]], 'assigned_trips': [], 'status': 'Active', 'depot': [-85.642907, 42.2749172], 'pickups_deliveries': [], 'demands': [0]}, {'bus_id': '31', 'capacity': 24, 'current_location': [-85.4275675, 42.2873505], 'locations': [], 'route': [], 'time_windows': [[0, 1440]], 'assigned_trips': [], 'status': 'Active', 'depot': [-85.4275675, 42.2873505], 'pickups_deliveries': [], 'demands': [0]}, {'bus_id': '32', 'capacity': 24, 'current_location': [-85.6495691, 42.2421546], 'locations': [], 'route': [], 'time_windows': [[0, 1440]], 'assigned_trips': [], 'status': 'Active', 'depot': [-85.6495691, 42.2421546], 'pickups_deliveries': [], 'demands': [0]}, {'bus_id': '33', 'capacity': 24, 'current_location': [-85.6421558, 42.2899382], 'locations': [], 'route': [], 'time_windows': [[0, 1440]], 'assigned_trips': [], 'status': 'Active', 'depot': [-85.6421558, 42.2899382], 'pickups_deliveries': [], 'demands': [0]}, {'bus_id': '34', 'capacity': 24, 'current_location': [-85.70643, 42.293878], 'locations': [], 'route': [], 'time_windows': [[0, 1440]], 'assigned_trips': [], 'status': 'Active', 'depot': [-85.70643, 42.293878], 'pickups_deliveries': [], 'demands': [0]}, {'bus_id': '35', 'capacity': 24, 'current_location': [-85.5307056, 42.120423], 'locations': [], 'route': [], 'time_windows': [[0, 1440]], 'assigned_trips': [], 'status': 'Active', 'depot': [-85.5307056, 42.120423], 'pickups_deliveries': [], 'demands': [0]}, {'bus_id': '36', 'capacity': 24, 'current_location': [-85.6478465, 42.1707126], 'locations': [], 'route': [], 'time_windows': [[0, 1440]], 'assigned_trips': [], 'status': 'Active', 'depot': [-85.6478465, 42.1707126], 'pickups_deliveries': [], 'demands': [0]}, {'bus_id': '37', 'capacity': 24, 'current_location': [-85.6137927, 42.1494793], 'locations': [], 'route': [], 'time_windows': [[0, 1440]], 'assigned_trips': [], 'status': 'Active', 'depot': [-85.6137927, 42.1494793], 'pickups_deliveries': [], 'demands': [0]}, {'bus_id': '38', 'capacity': 24, 'current_location': [-85.6259584, 42.3023157], 'locations': [], 'route': [], 'time_windows': [[0, 1440]], 'assigned_trips': [], 'status': 'Active', 'depot': [-85.6259584, 42.3023157], 'pickups_deliveries': [], 'demands': [0]}, {'bus_id': '39', 'capacity': 24, 'current_location': [-85.6836554, 42.2523655], 'locations': [], 'route': [], 'time_windows': [[0, 1440]], 'assigned_trips': [], 'status': 'Active', 'depot': [-85.6836554, 42.2523655], 'pickups_deliveries': [], 'demands': [0]}, {'bus_id': '40', 'capacity': 24, 'current_location': [-85.6032281, 42.1642518], 'locations': [], 'route': [], 'time_windows': [[0, 1440]], 'assigned_trips': [], 'status': 'Active', 'depot': [-85.6032281, 42.1642518], 'pickups_deliveries': [], 'demands': [0]}, {'bus_id': '41', 'capacity': 24, 'current_location': [-85.6142273, 42.2050614], 'locations': [], 'route': [], 'time_windows': [[0, 1440]], 'assigned_trips': [], 'status': 'Active', 'depot': [-85.6142273, 42.2050614], 'pickups_deliveries': [], 'demands': [0]}]

    for bus in buses:
        created_bus = create_bus(bus)
        print("Created Bus:", created_bus.bus_id)
    print("Created all buses")
    return jsonify({"message": "Database restarted"}), 200


def get_trip_updates(trip_id):
    # print("trip_id: " + str(trip_id))
    # get trip (ride request) from db
    trip = get_ride_by_id(trip_id)
    # print("trip: " + str(trip))
    #  get bus from trip
    # trip.bus is a reference field (ObjectId) to the bus document
    bus = get_bus_by_id(trip.bus.bus_id)
    # get route from bus
    route = bus.route
    # remove first and last locations from route
    route = route[1:-1]
    # print("route: " + str(route))

    # get locations from bus
    locations = bus.locations
    # print("locations: " + str(locations))
    # get current location from bus
    current_location = bus.current_location
    # convert current location to float
    current_location = [float(i) for i in current_location]
    # print("current_location: " + str(current_location))
    # arrange locations in the order of the route
    ordered_locations = []
    # print("route: " + str(route))
    for i in route:
        ordered_locations.append(locations[i-1])
    # append current location to the beginning of the list
    current_location_entry = {
        "trip_id": trip.id, "action": "current_location", "coordinates": current_location}
    ordered_locations.insert(0, current_location_entry)
    # print("ordered_locations: " + str(ordered_locations))
    # get list of locations from current location to pickup location
    pickup_location = {"trip_id": trip.id, "action": "pickup",
                       "coordinates": [float(i) for i in trip.start_location]}
    if pickup_location  in ordered_locations:
        locations_to_pickup = ordered_locations[0:ordered_locations.index(
            pickup_location)+1]    
    else:
        locations_to_pickup = [ordered_locations[0]]
    # print("locations_to_pickup: " + str(locations_to_pickup))
    # get list of locations from pickup location to dropoff location
    dropoff_location = {"trip_id": trip.id, "action": "dropoff",
                        "coordinates": [float(i) for i in trip.end_location]}
    if dropoff_location in ordered_locations:
        if pickup_location in ordered_locations:
            locations_to_dropoff = ordered_locations[ordered_locations.index(
                pickup_location):ordered_locations.index(dropoff_location)+1]
        else:
            locations_to_dropoff = ordered_locations[0:ordered_locations.index(
                dropoff_location)+1]
    else:
        locations_to_dropoff = [ordered_locations[0]]

    # print("locations_to_dropoff: " + str(locations_to_dropoff))
    if len(locations_to_pickup) == 1:
        distance_to_pickup = 0
        duration_to_pickup = 0
        path_to_pickup = []
    else:
        distance_to_pickup, duration_to_pickup, path_to_pickup = calcluate_trip_parmaters(
            [i["coordinates"] for i in locations_to_pickup])
        
    if len(locations_to_dropoff) == 1:
        distance_to_dropoff = 0
        duration_to_dropoff = 0
        path_to_dropoff = []
    else:
        distance_to_dropoff, duration_to_dropoff, path_to_dropoff = calcluate_trip_parmaters(
            [i["coordinates"] for i in locations_to_dropoff])
    # print("distance_to_pickup: " + str(distance_to_pickup))
    # print("duration_to_pickup: " + str(duration_to_pickup))
    # print("path_to_pickup: " + str(path_to_pickup))
    # print("distance_to_dropoff: " + str(distance_to_dropoff))
    # print("duration_to_dropoff: " + str(duration_to_dropoff))
    # print("path_to_dropoff: " + str(path_to_dropoff))
    return distance_to_pickup, duration_to_pickup, path_to_pickup, distance_to_dropoff, duration_to_dropoff, path_to_dropoff


def calcluate_trip_parmaters(locations_list):
    MAPBOX_TOKEN = "pk.eyJ1IjoiYWhtZWR5MTU1MjAwIiwiYSI6ImNscHU2anR0cjBrMjYyam1samJqN3Y5ZHcifQ.rI8SUfxadkqVpvemVZdvPw"
    # print("locations_list: " + str(locations_list))
    # get duration between stops
    max_locations_list = 25  # Maximum number of locations_list per API request
    # Number of API requests needed
    num_requests = (len(locations_list) - 1) // (max_locations_list - 1) + 1
    distance = 0
    duration = 0
    path = []
    # print("num_requests: " + str(num_requests))
    for req in range(num_requests):
        start = req * (max_locations_list - 1)
        end = min(start + max_locations_list, len(locations_list))
        # print("Trial one:", start, end)
        URL = 'https://api.mapbox.com/directions/v5/mapbox/driving/'
        for i in range(start, end):
            URL += "{},{};".format(locations_list[i][0], locations_list[i][1])

        URL = URL[:-1]
        URL += "?alternatives=false&geometries=geojson&language=en&overview=full&steps=false&access_token=pk.eyJ1IjoiYWhtZWR5MTU1MjAwIiwiYSI6ImNscHU2anR0cjBrMjYyam1samJqN3Y5ZHcifQ.rI8SUfxadkqVpvemVZdvPw"
        # print("URL: " + str(URL))
        response = requests.get(URL)

        if response.status_code == 200:
            data = response.json()
            # distance+=data['routes'][0]['distance']*0.000621371 # in miles
            distance += data['routes'][0]['distance']/1000  # in km
            duration += data['routes'][0]['duration']/60  # in minutes
            # Extract the geometry
            path_coordinates = data['routes'][0]['geometry']['coordinates']
            path.extend(path_coordinates)
    return distance, duration, path


def get_distance_between_two_loc(loc1, loc2):

    URL = 'https://api.mapbox.com/directions/v5/mapbox/driving/'
    URL += "{},{};{},{}".format(loc1[0], loc1[1], loc2[0], loc2[1])
    URL = URL[:-1]
    URL += "?alternatives=false&geometries=geojson&language=en&overview=full&steps=false&access_token=pk.eyJ1IjoiYWhtZWR5MTU1MjAwIiwiYSI6ImNscHU2anR0cjBrMjYyam1samJqN3Y5ZHcifQ.rI8SUfxadkqVpvemVZdvPw"

    response = requests.get(URL)

    distance = 0
    duration = 0
    path = []

    if response.status_code == 200:
        data = response.json()
        # distance += data['routes'][0]['distance'] * 0.000621371 # in miles
        distance += data['routes'][0]['distance'] / 1000  # in km
        duration += data['routes'][0]['duration'] / 60  # in minutes
        path_coordinates = data['routes'][0]['geometry']['coordinates']
        path.extend(path_coordinates)

    return distance, duration, path


if __name__ == "__main__":
    ride_request_bp.run(debug=True)
