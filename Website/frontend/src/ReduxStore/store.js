import { createStore } from "redux";
import rootReducer from "./reducer";

const rootStore = createStore(rootReducer);

export default rootStore;
