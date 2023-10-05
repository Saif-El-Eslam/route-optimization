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


# Input: list of locations


def VRP_pickup_dropoff_TW(
    df, max_pickup_delay=30, max_dropoff_delay=30, waiting_time=1, capacity=24
):
    """Entry point of the program."""
    data = create_data_model(
        df, max_pickup_delay, max_dropoff_delay, waiting_time, capacity
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
        routing.AddVariableMinimizedByFinalizer(time_dimension.CumulVar(routing.End(i)))

    # pickup and delivery
    for request in data["pickups_deliveries"]:
        pickup_index = manager.NodeToIndex(request[0])
        delivery_index = manager.NodeToIndex(request[1])
        routing.AddPickupAndDelivery(pickup_index, delivery_index)
        routing.solver().Add(
            routing.VehicleVar(pickup_index) == routing.VehicleVar(delivery_index)
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

    demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)
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
    search_parameters.time_limit.seconds = 30
    # solutions limit
    # search_parameters.solution_limit = 100

    solution = routing.SolveWithParameters(search_parameters)
    if solution:
        # print(routes)
        # print ("Time windows", data["time_windows"])
        routes = get_routes(solution, routing, manager)
        delays = get_delays(data, manager, routing, solution)
        return routes, get_total_distance(data, manager, routing, solution), delays
    else:
        # print("No solution found.")
        return [], 0, []


def create_data_model(
    locations, max_pickup_delay, max_dropoff_delay, waiting_time=1, capacity=24
):
    """Stores the data for the problem."""
    data = {}
    data["distance_matrix"] = get_direction_matrix_arc(locations)
    data["pickups_deliveries"] = [
        [i * 2 + 1, i * 2 + 2] for i in range(len(locations))
    ]  # TODO: could pass it to the function or the locations should be in order (pickup, dropoff, pickup, dropoff, ...)
    data["num_vehicles"] = 1
    data["depot"] = 0
    timematrix = [[int(t / 40 * 60) for t in row] for row in data["distance_matrix"]]

    # add waiting time to all time matrix values except the zero values
    for i in range(len(timematrix)):
        for j in range(len(timematrix)):
            if timematrix[i][j] != 0:
                timematrix[i][j] += waiting_time

    data["time_matrix"] = timematrix
    data["time_windows"] = get_time_windows(
        df, timematrix, max_pickup_delay, max_dropoff_delay
    )
    # demands is 0,1,-1,1,-1,1,-1
    data["demands"] = [0] + [1, -1] * len(locations)
    # capacity is 20 for all vehicles
    data["vehicle_capacities"] = [capacity for i in range(data["num_vehicles"])]
    # print(data)
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
        + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2
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
            distance_matrix[i][j] = int(distance)
    return distance_matrix  # in kilometers


def get_time_windows(df, timematrix, max_pickup_delay, max_dropoff_delay):
    """
    Get the time windows from the dataframe
    :param df: the dataframe
    :return: a list of time windows
    """
    # time window list for a pickup is (request time, request time + 10)
    # time window list for a delivery is (request time + time matrix[pickup][delivery], request time + time matrix[pickup][delivery] + 10)
    time_windows = []
    # append the time window for the first pickup (depot)
    start_time = df["PickUp Time"].iloc[0]
    time_windows.append((0, 0))  # the depot has no time window
    for i in range(len(df)):
        time_windows.append(
            (
                df["PickUp Time"].iloc[i] - start_time,
                df["PickUp Time"].iloc[i] - start_time + max_pickup_delay,
            )
        )
        # time_windows.append((df["PickUp Time"].iloc[i] + timematrix[2*i+1][2*i+2] - start_time, df["PickUp Time"].iloc[i] + timematrix[2*i+1][2*i+2] - start_time + 15))
        # TODO: the next line solved the problem, we can add it to trips causing problems
        time_windows.append(
            (
                df["PickUp Time"].iloc[i]
                + timematrix[2 * i + 1][2 * i + 2]
                - start_time,
                df["PickUp Time"].iloc[i]
                + timematrix[2 * i + 1][2 * i + 2]
                - start_time
                + max_dropoff_delay,
            )
        )
    return time_windows


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
