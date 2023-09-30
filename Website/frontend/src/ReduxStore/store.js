import { createStore } from "redux";
import rideReducer from "./reducer";

const rideStore = createStore(rideReducer);

export default rideStore;
