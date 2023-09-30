import * as actions from "./actionTypes";

// import { combineReducers } from "redux";

// function userReducer(state = {}, action) {
//   switch (action.type) {
//     case "SET_USER":
//       return {
//         ...state,
//         user: action.payload,
//       };
//     default:
//       return state;
//   }
// }

export default function rideReducer(state = {}, action) {
  switch (action.type) {
    case actions.SET_RIDE:
      return {
        ...state,
        ride: action.payload,
      };
    case actions.UPDATE_RIDE:
      return {
        ...state,
        ride: {
          ...state.ride,
          ...action.payload,
        },
      };
    default:
      return state;
  }
}

// export default combineReducers({
//   userReducer,
//   rideReducer,
// });
