import rideStore from "./store";
import * as actions from "./actionTypes";

// initialize rideStore with a test ride
setRide({
  pickupLocation: {
    address: "123 Main St San Diego CA",
    coordinates: [-117.161084, 32.715736],
  },
  dropoffLocation: {
    address: "456 Main St San Diego CA",
    coordinates: [-117.161084, 32.715736],
  },
  time: "ASAP",
  passengerCount: 1,
});

function setRide(ride) {
  rideStore.dispatch({
    type: actions.SET_RIDE,
    payload: ride,
  });
}

function getRide() {
  return rideStore.getState().ride;
}

function updateRide(ride) {
  rideStore.dispatch({
    type: actions.UPDATE_RIDE,
    payload: ride,
  });
}

export { setRide, updateRide, getRide };
