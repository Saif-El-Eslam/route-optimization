import { createStore } from "redux";
import rideReducer from "./reducer";
import storage from "redux-persist/lib/storage";

const persistConfig = {
  key: "main-root",
  storage,
};

const rideStore = createStore(rideReducer);

export default rideStore;
