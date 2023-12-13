# route-optimization
TODO:
- Check authorization for all endpoints (Mostly done)
- Passenger count > 1
- Upon current location update, check if the new location is within the radius of the next stop. If so, update the current location to the next stop and remove the stop from the list of stops. This will reduce the number of stops to be made.
- Only reload the markers on the map when bus location is updated(don't reload the whole map)
- Handle trips ar 12am
- Put the Tokens in a config file (backend)
- Make the map refresh static (remove the flyTo animation)
- Implement other pages (About, Contact, User Settings, etc.)

FIXME: 
- the current location is not being updated in the rider's app

<!-- Testing -->
- One trip:
locations:[pickup, dropoff] .... in the model: [current_location, pickup, dropoff]
route:[0, 1,2,0]
demands:[0,1,-1]
pickup_deliveries:[[1,2]]
time_windows:[[0, 0], [0, 10], [10, 20]]

---After the first stop---
locations:[dropoff] .... in the model: [current_location, dropoff]
route:[0, 2,0]
demands:[0,-1]
pickup_deliveries:[[]]
time_windows:[[0, 0], [10, 20]]


TODO: try to test the "update current location" feature by postman
