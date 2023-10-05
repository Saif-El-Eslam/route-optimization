from db_connection import db
from schemas import *
from services import *


if __name__ == "__main__":
    # Example: Create  10 buses
    # bus_data = {
    #     "bus_id": "Bus1",
    #     "capacity": 20,
    #     "current_location": [-85.617046, 42.3030528],  # [longitude, latitude]
    #     "route": [],  # [longitude, latitude]
    #     "assigned_trips": [],
    #     "status": "Active",
    # }

    # for i in range(1, 11):
    #     bus_data["bus_id"] = "Bus" + str(i)
    #     created_bus = create_bus(bus_data)

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
    # print("Created Rider Request:", created_rider_request.rider_id)

    # Example: Get a rider request by ID
    retrieved_rider_request = get_ride_request("Rider1")  # "Rider1
    print("Retrieved Rider Request:", retrieved_rider_request.rider_id)

    # # Example: Update a rider request
    update_data = {"status": "Completed"}
    updated_rider_request = update_ride_request(
        retrieved_rider_request.rider_id, update_data
    )
    print("Updated Rider Request Status:", updated_rider_request.status)
