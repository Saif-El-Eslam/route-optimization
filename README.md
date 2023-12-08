# route-optimization
TODO:
- Check authorization for all endpoints (Mostly done)
- Passenger count > 1
- Upon current location update, check if the new location is within the radius of the next stop. If so, update the current location to the next stop and remove the stop from the list of stops. This will reduce the number of stops to be made.
- Only reload the markers on the map when bus location is updated(don't reload the whole map)
- Handle trips ar 12am
- Put the Tokens in a config file (backend)
- Make the map refresh static (remove the flyTo animation)