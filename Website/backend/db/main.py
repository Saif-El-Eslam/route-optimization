from db_connection import db
from schemas import *
from services import *


if __name__ == "__main__":
    # Example: Create  10 buses
    # bus_data = {
    #     "bus_id": "Bus1",
    #     "capacity": 20,
    #     "current_location": [-85.617046, 42.3030528],  # [longitude, latitude]
    #     "route": [], "time_windows" :[],  # [longitude, latitude]
    #     "assigned_trips": [],
    #     "status": "Active",
    # }
    buses = [
        {
            "bus_id": "1",
            "capacity": 24,
            "current_location": [-85.5473919, 42.3226625],
            "route": [],
            "time_windows":[],

            "assigned_trips": [],
            "status": "Available",
            "depot": [-85.5473919, 42.3226625],
        },
        {
            "bus_id": "2",
            "capacity": 24,
            "current_location": [-85.6880877, 42.2666994],
            "route": [],
            "assigned_trips": [],
            "status": "Available",
            "depot": [-85.6880877, 42.2666994],
        },
        {
            "bus_id": "3",
            "capacity": 24,
            "current_location": [-85.5624162, 42.2977748],
            "route": [],
            "time_windows":[],
            "assigned_trips": [],
            "status": "Available",
            "depot": [-85.5624162, 42.2977748],
        },
        {
            "bus_id": "4",
            "capacity": 24,
            "current_location": [-85.5940978, 42.2470918],
            "route": [],
            "time_windows":[],
            "assigned_trips": [],
            "status": "Available",
            "depot": [-85.5940978, 42.2470918],
        },
        {
            "bus_id": "5",
            "capacity": 24,
            "current_location": [-85.6102235, 42.2845248],
            "route": [],
            "time_windows":[],
            "assigned_trips": [],
            "status": "Available",
            "depot": [-85.6102235, 42.2845248],
        },
        {
            "bus_id": "6",
            "capacity": 24,
            "current_location": [-85.5355127, 42.334607],
            "route": [],
            "time_windows":[],
            "assigned_trips": [],
            "status": "Available",
            "depot": [-85.5355127, 42.334607],
        },
        {
            "bus_id": "7",
            "capacity": 24,
            "current_location": [-85.5945787, 42.2475577],
            "route": [],
            "time_windows":[],
            "assigned_trips": [],
            "status": "Available",
            "depot": [-85.5945787, 42.2475577],
        },
        {
            "bus_id": "8",
            "capacity": 24,
            "current_location": [-85.5544953, 42.2991703],
            "route": [],
            "time_windows":[],
            "assigned_trips": [],
            "status": "Available",
            "depot": [-85.5544953, 42.2991703],
        },
        {
            "bus_id": "9",
            "capacity": 24,
            "current_location": [-85.5636076, 42.2513353],
            "route": [],
            "time_windows":[],
            "assigned_trips": [],
            "status": "Available",
            "depot": [-85.5636076, 42.2513353],
        },
        {
            "bus_id": "10",
            "capacity": 24,
            "current_location": [-85.6087517, 42.2077529],
            "route": [],
            "time_windows":[],
            "assigned_trips": [],
            "status": "Available",
            "depot": [-85.6087517, 42.2077529],
        },
        {
            "bus_id": "11",
            "capacity": 24,
            "current_location": [-85.457795, 42.399715],
            "route": [],
            "time_windows":[],
            "assigned_trips": [],
            "status": "Available",
            "depot": [-85.457795, 42.399715],
        },
        {
            "bus_id": "12",
            "capacity": 24,
            "current_location": [-85.4727853, 42.1543539],
            "route": [],
            "time_windows":[],
            "assigned_trips": [],
            "status": "Available",
            "depot": [-85.4727853, 42.1543539],
        },
        {
            "bus_id": "13",
            "capacity": 24,
            "current_location": [-85.5550967, 42.2581612],
            "route": [],
            "time_windows":[],
            "assigned_trips": [],
            "status": "Available",
            "depot": [-85.5550967, 42.2581612],
        },
        {
            "bus_id": "14",
            "capacity": 24,
            "current_location": [-85.6320449, 42.2964597],
            "route": [],
            "time_windows":[],
            "assigned_trips": [],
            "status": "Available",
            "depot": [-85.6320449, 42.2964597],
        },
        {
            "bus_id": "15",
            "capacity": 24,
            "current_location": [-85.4683159, 42.3747781],
            "route": [],
            "time_windows":[],
            "assigned_trips": [],
            "status": "Available",
            "depot": [-85.4683159, 42.3747781],
        },
        {
            "bus_id": "16",
            "capacity": 24,
            "current_location": [-85.5859105, 42.2829969],
            "route": [],
            "time_windows":[],
            "assigned_trips": [],
            "status": "Available",
            "depot": [-85.5859105, 42.2829969],
        },
        {
            "bus_id": "17",
            "capacity": 24,
            "current_location": [-85.409809, 42.2933292],
            "route": [],
            "time_windows":[],
            "assigned_trips": [],
            "status": "Available",
            "depot": [-85.409809, 42.2933292],
        },
        {
            "bus_id": "18",
            "capacity": 24,
            "current_location": [-85.5033838, 42.1410135],
            "route": [],
            "time_windows":[],
            "assigned_trips": [],
            "status": "Available",
            "depot": [-85.5033838, 42.1410135],
        },
        {
            "bus_id": "19",
            "capacity": 24,
            "current_location": [-85.5221051, 42.3280919],
            "route": [],
            "time_windows":[],
            "assigned_trips": [],
            "status": "Available",
            "depot": [-85.5221051, 42.3280919],
        },
        {
            "bus_id": "20",
            "capacity": 24,
            "current_location": [-85.5844838, 42.1729487],
            "route": [],
            "time_windows":[],
            "assigned_trips": [],
            "status": "Available",
            "depot": [-85.5844838, 42.1729487],
        },
        {
            "bus_id": "21",
            "capacity": 24,
            "current_location": [-85.7262985, 42.2457494],
            "route": [],
            "time_windows":[],
            "assigned_trips": [],
            "status": "Available",
            "depot": [-85.7262985, 42.2457494],
        },
        {
            "bus_id": "22",
            "capacity": 24,
            "current_location": [-85.5794339, 42.262203],
            "route": [],
            "time_windows":[],
            "assigned_trips": [],
            "status": "Available",
            "depot": [-85.5794339, 42.262203],
        },
        {
            "bus_id": "23",
            "capacity": 24,
            "current_location": [-85.5316711, 42.3407718],
            "route": [],
            "time_windows":[],
            "assigned_trips": [],
            "status": "Available",
            "depot": [-85.5316711, 42.3407718],
        },
        {
            "bus_id": "24",
            "capacity": 24,
            "current_location": [-85.7507622, 42.2836978],
            "route": [],
            "time_windows":[],
            "assigned_trips": [],
            "status": "Available",
            "depot": [-85.7507622, 42.2836978],
        },
        {
            "bus_id": "25",
            "capacity": 24,
            "current_location": [-85.5585162, 42.3321206],
            "route": [],
            "time_windows":[],
            "assigned_trips": [],
            "status": "Available",
            "depot": [-85.5585162, 42.3321206],
        },
        {
            "bus_id": "26",
            "capacity": 24,
            "current_location": [-85.6114028, 42.2036211],
            "route": [],
            "time_windows":[],
            "assigned_trips": [],
            "status": "Available",
            "depot": [-85.6114028, 42.2036211],
        },
        {
            "bus_id": "27",
            "capacity": 24,
            "current_location": [-85.7507622, 42.2836978],
            "route": [],
            "time_windows":[],
            "assigned_trips": [],
            "status": "Available",
            "depot": [-85.7507622, 42.2836978],
        },
        {
            "bus_id": "28",
            "capacity": 24,
            "current_location": [-85.5701549, 42.2196805],
            "route": [],
            "time_windows":[],
            "assigned_trips": [],
            "status": "Available",
            "depot": [-85.5701549, 42.2196805],
        },
        {
            "bus_id": "29",
            "capacity": 24,
            "current_location": [-85.4735514, 42.3071286],
            "route": [],
            "time_windows":[],
            "assigned_trips": [],
            "status": "Available",
            "depot": [-85.4735514, 42.3071286],
        },
        {
            "bus_id": "30",
            "capacity": 24,
            "current_location": [-85.642907, 42.2749172],
            "route": [],
            "time_windows":[],
            "assigned_trips": [],
            "status": "Available",
            "depot": [-85.642907, 42.2749172],
        },
        {
            "bus_id": "31",
            "capacity": 24,
            "current_location": [-85.4275675, 42.2873505],
            "route": [],
            "time_windows":[],
            "assigned_trips": [],
            "status": "Available",
            "depot": [-85.4275675, 42.2873505],
        },
        {
            "bus_id": "32",
            "capacity": 24,
            "current_location": [-85.6495691, 42.2421546],
            "route": [],
            "time_windows":[],
            "assigned_trips": [],
            "status": "Available",
            "depot": [-85.6495691, 42.2421546],
        },
        {
            "bus_id": "33",
            "capacity": 24,
            "current_location": [-85.6421558, 42.2899382],
            "route": [],
            "time_windows":[],
            "assigned_trips": [],
            "status": "Available",
            "depot": [-85.6421558, 42.2899382],
        },
        {
            "bus_id": "34",
            "capacity": 24,
            "current_location": [-85.70643, 42.293878],
            "route": [],
            "time_windows":[],
            "assigned_trips": [],
            "status": "Available",
            "depot": [-85.70643, 42.293878],
        },
        {
            "bus_id": "35",
            "capacity": 24,
            "current_location": [-85.5307056, 42.120423],
            "route": [],
            "time_windows":[],
            "assigned_trips": [],
            "status": "Available",
            "depot": [-85.5307056, 42.120423],
        },
        {
            "bus_id": "36",
            "capacity": 24,
            "current_location": [-85.6478465, 42.1707126],
            "route": [],
            "time_windows":[],
            "assigned_trips": [],
            "status": "Available",
            "depot": [-85.6478465, 42.1707126],
        },
        {
            "bus_id": "37",
            "capacity": 24,
            "current_location": [-85.6137927, 42.1494793],
            "route": [],
            "time_windows":[],
            "assigned_trips": [],
            "status": "Available",
            "depot": [-85.6137927, 42.1494793],
        },
        {
            "bus_id": "38",
            "capacity": 24,
            "current_location": [-85.6259584, 42.3023157],
            "route": [],
            "time_windows":[],
            "assigned_trips": [],
            "status": "Available",
            "depot": [-85.6259584, 42.3023157],
        },
        {
            "bus_id": "39",
            "capacity": 24,
            "current_location": [-85.6836554, 42.2523655],
            "route": [],
            "time_windows":[],
            "assigned_trips": [],
            "status": "Available",
            "depot": [-85.6836554, 42.2523655],
        },
        {
            "bus_id": "40",
            "capacity": 24,
            "current_location": [-85.6032281, 42.1642518],
            "route": [],
            "time_windows":[],
            "assigned_trips": [],
            "status": "Available",
            "depot": [-85.6032281, 42.1642518],
        },
        {
            "bus_id": "41",
            "capacity": 24,
            "current_location": [-85.6142273, 42.2050614],
            "route": [],
            "time_windows":[],
            "assigned_trips": [],
            "status": "Available",
            "depot": [-85.6142273, 42.2050614],
        },
    ]

    for bus in buses:
        created_bus = create_bus(bus)
        print("Created Bus:", created_bus.bus_id)


#####################################################################################

# # Example: Get a bus by ID
# retrieved_bus = get_bus("Bus1")  # "Bus1
# print("Retrieved Bus:", retrieved_bus.bus_id)

# # # Example: Update a bus
# update_data = {"current_location": [-85.617046, 42.3030529]}
# updated_bus = update_bus(retrieved_bus.bus_id, update_data)
# print("Updated Bus Location:", updated_bus.current_location)

# # # Example: Delete a bus
# delete_bus(retrieved_bus.bus_id)
# print("Bus Deleted")

# Create rider request
# rider_request_data = {
#     "rider_id": "Rider1",
#     "request_time": "2021-03-01 12:00:00",
#     "start_location": [-85.617046, 42.3030528],  # [longitude, latitude
#     "end_location": [-85.617046, 42.3030528],  # [longitude, latitude]
#     "status": "Pending",
# }
# created_rider_request = create_ride_request(rider_request_data)
# print("Created Rider Request:", creسted_rider_request.rider_id)

# Example: Get a rider request by ID
# retrieved_rider_request = get_ride_request("Rider1")  # "Rider1
# print("Retrieved Rider Request:", retrieved_rider_request.rider_id)

# # # Example: Update a rider request
# update_data = {"status": "Completed"}
# updated_rider_request = update_ride_request(
#     retrieved_rider_request.rider_id, update_data
# )
# print("Updated Rider Request Status:", updated_rider_request.status)
