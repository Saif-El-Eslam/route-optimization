# route-optimization
TODO:
- Authorization of requests (like in update location post request)
- Add .env file for configuration
- Passenger count > 1
- Add more tests
- Upon current location update, check if the new location is within the radius of the next stop. If so, update the current location to the next stop and remove the stop from the list of stops. This will reduce the number of stops to be made.
- Allow user to request only one ride at a time (when login, check if user has any active rides, if so, don't allow user to request another ride) (you can make the url/ride/ride_id instead of storing the ride_id and its info in the session)
- Only reload the markers on the map when bus location is updated(don't reload the whole map)
