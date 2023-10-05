import "./App.css";
import Home from "./Pages/Home/Home";
import GetLocations from "./Pages/GetLocations/GetLocations";
import RequestRide from "./Pages/Ride/Ride";
import SignUp from "./Pages/SignUp/SignUp";
// import Login from "./Pages/Login/Login";

import { BrowserRouter, Routes, Route } from "react-router-dom";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/get-locations" element={<GetLocations />} />
        <Route path="/ride" element={<RequestRide />} />
        {/* <Route path="/rider/:id" element={<Rider />} />
        <Route path="/driver/:id" element={<Driver />} /> */}
        <Route path="/signup" element={<SignUp />} />
        {/* <Route path="/login" element={<Login />} /> */}
      </Routes>
    </BrowserRouter>
  );
}

export default App;
