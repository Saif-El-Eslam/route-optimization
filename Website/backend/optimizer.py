# Imports
import math
import pandas as pd
import googlemaps
from datetime import datetime
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import requests
import os
import networkx as nx
import tkinter as tk
from tkintermapview import TkinterMapView

# Global variables
gmaps = googlemaps.Client(key="AIzaSyCKNRwMEYukzka5pRhiPL8LrJG_U4qlW2A")
MAPBOX_TOKEN = "pk.eyJ1IjoiYWhtZWR5MTU1MjAwIiwiYSI6ImNsamw4cDM3NDAzejAzZG1uc2Y4MGJ4aWIifQ.9z0OvMdr2pISeiDFf4ufTw"


def get_total_distance(data, manager, routing, solution):
    """Calculates and returns the total distance of all routes."""
    total_distance = 0
    for vehicle_id in range(data["num_vehicles"]):
        index = routing.Start(vehicle_id)
        route_distance = 0
        while not routing.IsEnd(index):
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id)
        total_distance += route_distance
    return total_distance


def get_routes(solution, routing, manager):
    """Get vehicle routes from a solution and store them in an array."""
    routes = []
    for route_nbr in range(routing.vehicles()):
        index = routing.Start(route_nbr)
        route = [manager.IndexToNode(index)]
        while not routing.IsEnd(index):
            index = solution.Value(routing.NextVar(index))
            route.append(manager.IndexToNode(index))
        routes.append(route)
    return routes


def get_delays(data, manager, routing, solution):
    """Get vehicle routes from a solution and store them in an array."""
    # print("Time Matrix:", data["time_matrix"])
    # print("Time Window:", data["time_windows"])
    delays = []
    time_dimension = routing.GetDimensionOrDie('time')
    for route_nbr in range(routing.vehicles()):
        index = routing.Start(route_nbr)
        route = get_routes(solution, routing, manager)[route_nbr]
        while not routing.IsEnd(index):
            time_var = time_dimension.CumulVar(index)
            delays.append((solution.Min(time_var), solution.Max(time_var)))
            index = solution.Value(routing.NextVar(index))
        # print("delays",delays) #these are the arrival times corresponding to the route sequence
        # FIXME: the following code doesn't seem to be right

        # rearrange delays according to route
        zipped = zip(route, delays)
        zipped = sorted(zipped, key=lambda x: x[0])
        sorted_delays = [pair[1] for pair in zipped]
        # print("sorted",sorted_delays)
        output_delays = []
        for i in range(len(sorted_delays)):
            output_delays.append(
                sorted_delays[i][0] - data["time_windows"][i][0])

        # pop first element to get rid of depot
        output_delays.pop(0)
        # print("Delays:", output_delays)

    return output_delays


# Input: list of locations
def VRP_pickup_dropoff_TW(
    locations, time_window, max_pickup_delay=30, max_dropoff_delay=30, waiting_time=1, capacity=24
):
    """Entry point of the program.
    Args:
        locations: list of locations where each location is a tuple of (latitude, longitude)
        time_window: list of time windows where each time window is a tuple of (start_time, end_time)
        max_pickup_delay: maximum delay for pickup in minutes
        max_dropoff_delay: maximum delay for dropoff in minutes
        waiting_time: waiting time in minutes
        capacity: capacity of the vehicle
    Returns:
        routes: list of routes where each route is a list of locations
        total_distance: total distance of the routes in kilometers
        delays: list of delays for each location in minutes
    """

    data = create_data_model(
        locations, time_window, max_pickup_delay, max_dropoff_delay, waiting_time, capacity
    )
    manager = pywrapcp.RoutingIndexManager(
        len(data["distance_matrix"]), data["num_vehicles"], data["depot"]
    )
    routing = pywrapcp.RoutingModel(manager)

    def time_callback(from_index, to_index):
        """Returns the manhattan distance between the two nodes."""
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data["time_matrix"][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(time_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    time = "time"
    routing.AddDimension(
        transit_callback_index,  # transit callback index
        60,  # allow waiting time
        1440,  # maximum time per vehicle
        False,  # Don't force start cumul to zero.
        time,
    )
    time_dimension = routing.GetDimensionOrDie(time)
    time_dimension.SetGlobalSpanCostCoefficient(100)

    # Add time window constraints for each location except depot.
    for location_idx, time_window in enumerate(data["time_windows"]):
        if location_idx == 0:
            continue
        index = manager.NodeToIndex(location_idx)
        # print(int(time_window[0]), int(time_window[1]))
        time_dimension.CumulVar(index).SetRange(
            int(time_window[0]), int(time_window[1])
        )

    # Add time window constraints for each vehicle start node.
    for vehicle_id in range(data["num_vehicles"]):
        index = routing.Start(vehicle_id)
        time_dimension.CumulVar(index).SetRange(
            data["time_windows"][0][0], data["time_windows"][0][1]
        )

    # Instantiate route start and end times to produce feasible times.
    for i in range(data["num_vehicles"]):
        routing.AddVariableMinimizedByFinalizer(
            time_dimension.CumulVar(routing.Start(i))
        )
        routing.AddVariableMinimizedByFinalizer(
            time_dimension.CumulVar(routing.End(i)))

    # pickup and delivery
    for request in data["pickups_deliveries"]:
        pickup_index = manager.NodeToIndex(request[0])
        delivery_index = manager.NodeToIndex(request[1])
        routing.AddPickupAndDelivery(pickup_index, delivery_index)
        routing.solver().Add(
            routing.VehicleVar(
                pickup_index) == routing.VehicleVar(delivery_index)
        )
        routing.solver().Add(
            time_dimension.CumulVar(pickup_index)
            <= time_dimension.CumulVar(delivery_index)
        )
    # Capacity constraint

    def demand_callback(from_index):
        """Returns the demand of the node."""
        from_node = manager.IndexToNode(from_index)
        return data["demands"][from_node]

    demand_callback_index = routing.RegisterUnaryTransitCallback(
        demand_callback)
    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,  # null capacity slack
        data["vehicle_capacities"],  # vehicle maximum capacities
        True,  # start cumul to zero
        "Capacity",
    )

    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PARALLEL_CHEAPEST_INSERTION
    )
    # time limit
    # search_parameters.time_limit.seconds = 30
    # solutions limit
    # search_parameters.solution_limit = 100
    print("Start solving...")
    solution = routing.SolveWithParameters(search_parameters)
    if solution:
        # print(routes)
        # print ("Time windows", data["time_windows"])
        routes = get_routes(solution, routing, manager)
        delays = get_delays(data, manager, routing, solution)
        return routes, get_total_distance(data, manager, routing, solution), delays
        # print("Solution found.")
        # return [], 0, []
    else:
        print("No solution found.")
        return [], 0, []


def create_data_model(
    locations, time_window, max_pickup_delay=30, max_dropoff_delay=30, waiting_time=1, capacity=24
):
    """Stores the data for the problem."""
    data = {}
    data["distance_matrix"] = get_direction_matrix_arc(locations)
    data["pickups_deliveries"] = [
        [i * 2 + 1, i * 2 + 2] for i in range(int(len(locations)/2))
    ]  # TODO: could pass it to the function or the locations should be in order (pickup, dropoff, pickup, dropoff, ...)
    data["num_vehicles"] = 1
    data["depot"] = 0
    timematrix = [[int(t / 40 * 60) for t in row]
                  for row in data["distance_matrix"]]

    # add waiting time to all time matrix values except the zero values
    for i in range(len(timematrix)):
        for j in range(len(timematrix)):
            if timematrix[i][j] != 0:
                timematrix[i][j] += waiting_time

    data["time_matrix"] = timematrix
    data["time_windows"] = time_window
    # demands is 0,1,-1,1,-1,1,-1
    data["demands"] = [0] + [1, -1] * int(len(locations) / 2)
    # capacity is 20 for all vehicles
    data["vehicle_capacities"] = [
        capacity for i in range(data["num_vehicles"])]
    print(data)
    return data


def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great-circle distance between two points using the haversine formula.
    :param lat1: Latitude of the first point in degrees
    :param lon1: Longitude of the first point in degrees
    :param lat2: Latitude of the second point in degrees
    :param lon2: Longitude of the second point in degrees
    :return: Distance between the two points in kilometers
    """
    # Convert latitude and longitude from degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Haversine formula
    delta_lat = lat2_rad - lat1_rad
    delta_lon = lon2_rad - lon1_rad
    a = (
        math.sin(delta_lat / 2) ** 2
        + math.cos(lat1_rad) * math.cos(lat2_rad) *
        math.sin(delta_lon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = 6371 * c  # Radius of the Earth in kilometers

    return distance  # in kilometers


def get_direction_matrix_arc(locations):
    """
    Get the distance matrix of a list of locations using arc distance (haversine formula)
    :param locations: a list of locations where each location is a tuple of (latitude, longitude)
    :return: a matrix of distance in kilometers
    """
    num_locations = len(locations)
    # Initialize an empty two-dimensional array to store the distance matrix
    distance_matrix = [[None] * num_locations for _ in range(num_locations)]
    for i in range(num_locations):
        for j in range(num_locations):
            lat1, lon1 = locations[i]
            lat2, lon2 = locations[j]
            distance = haversine(lat1, lon1, lat2, lon2)
            # for the first point in the row,make it 0
            if j == 0:
                distance_matrix[i][j] = 0
            else:
                distance_matrix[i][j] = int(distance)
    return distance_matrix  # in kilometers


def calculate_time_between_locations(loc1, loc2):
    # Make a directions request
    directions_result = gmaps.directions(loc1, loc2, mode="driving")

    # Extract the driving time from the response
    if directions_result and "legs" in directions_result[0]:
        leg = directions_result[0]["legs"][0]
        return leg["duration"]["value"]  # Duration in seconds

    # If directions request fails or time cannot be calculated, fall back to NetworkX
    G = nx.Graph()
    G.add_edge(loc1, loc2, weight=1)  # Add a dummy edge with weight 1
    try:
        return nx.shortest_path_length(G, loc1, loc2, weight="weight")
    except nx.NetworkXNoPath:
        return float("inf")  # Return infinity if no path exists


def main():
    # input : old route, time window
    # output : new route, total distance, delays
    # depot = [30.77305678190685, 30.813048152000523]
    # 1 :30.795700945482718,30.819262082140266
    # 2: 30.8140702192498, 30.819690604927697
    # 3: 30.77490006380151, 30.81398531217546
    # 4:  30.873275348454126, 30.811269362683074
    bus_test = {
        "bus_id": "2",
        "capacity": 1,
        "current_location": [30.77305678190685, 30.813048152000523],
        "locations": [(1, "pickup", [30.795700945482718, 30.819262082140266]),
                      (2, "dropoff", [30.8140702192498, 30.819690604927697]),
                      (3, "pickup", [30.77490006380151, 30.81398531217546]),
                      (4, "dropoff", [30.873275348454126, 30.811269362683074])],
        "route": [],
        "time_windows": [[0, 0], [0, 1440], [0, 1440], [0, 1440], [0, 1440]],
        "assigned_trips": [],
        "status": "Active",
        "depot": [30.77305678190685, 30.813048152000523]
    }
    locations = [bus_test["current_location"]] + [location[2]
                                                  for location in bus_test["locations"]]
    time_window = bus_test["time_windows"]
    max_pickup_delay = 15
    max_dropoff_delay = 15
    waiting_time = 1
    capacity = 24

    result = VRP_pickup_dropoff_TW(
        locations, time_window, max_pickup_delay, max_dropoff_delay, waiting_time, capacity
    )
    print(result)


if __name__ == "__main__":
    main()
