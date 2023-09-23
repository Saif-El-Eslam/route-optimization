from db_connection import db
from schemas import *
from services import *

if __name__ == "__main__":
    # Example: Create a new bus
    bus_data = {
        "bus_number": "Bus123",
        "capacity": 50,
        "current_location": "Station A",
        "status": "Active"
    }
    created_bus = create_bus(bus_data)
    print("Created Bus:", created_bus.bus_number)

    # Example: Get a bus by ID
    retrieved_bus = get_bus(created_bus.id)
    print("Retrieved Bus:", retrieved_bus.bus_number)

    # # Example: Update a bus
    update_data = {"current_location": "Station B"}
    updated_bus = update_bus(retrieved_bus.id, update_data)
    print("Updated Bus Location:", updated_bus.current_location)

    # # Example: Delete a bus
    delete_bus(retrieved_bus.id)
    print("Bus Deleted")
