# route-optimization
TODO:
- Check authorization for all endpoints (Mostly done)
- Try reloading the route only when the bus is moving not the whole map.( You can use map.getsource() and map.getlayer() to get the source and layer of the route and then use map.removeLayer() and map.removeSource() to remove the route and then add the new route using map.addSource() and map.addLayer() 
- Passenger count > 1
- Handle trips ar 12am
- Put the Tokens in a config file (backend)
- Enforce Strong Passwords
- Implement other pages (About, Contact, User Settings, etc.)


FIXME: 
- The current location is not being updated in the rider's app
- When the trip is over, the rider's app should be redirected to the home page and the session should be cleared

