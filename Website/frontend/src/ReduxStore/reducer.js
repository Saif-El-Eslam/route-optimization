import * as actions from "./actionTypes";

import { combineReducers } from "redux";

export default function rootReducer(state = {}, action) {
  switch (action.type) {
    case actions.SET_USER:
      return {
        ...state,
        user: action.payload,
      };
    case actions.UPDATE_USER:
      return {
        ...state,
        user: {
          ...state.user,
          ...action.payload,
        },
      };
    case actions.REMOVE_USER:
      return {
        ...state,
        user: {},
      };
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
