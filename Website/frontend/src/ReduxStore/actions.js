import rootStore from "./store";
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
  rootStore.dispatch({
    type: actions.SET_RIDE,
    payload: ride,
  });
}

function getRide() {
  return rootStore.getState().ride;
}

function updateRide(ride) {
  rootStore.dispatch({
    type: actions.UPDATE_RIDE,
    payload: ride,
  });
}

function setUser(user) {
  rootStore.dispatch({
    type: actions.SET_USER,
    payload: user,
  });
}

function getUser() {
  return rootStore.getState().user;
}

function updateUser(user) {
  rootStore.dispatch({
    type: actions.UPDATE_USER,
    payload: user,
  });
}

function removeUser() {
  rootStore.dispatch({
    type: actions.REMOVE_USER,
  });
}

export {
  setRide,
  updateRide,
  getRide,
  setUser,
  getUser,
  updateUser,
  removeUser,
};
