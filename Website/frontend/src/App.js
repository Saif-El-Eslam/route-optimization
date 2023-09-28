import "./App.css";
import Home from "./Pages/Home/Home";
import GetLocations from "./Pages/GetLocations/GetLocations";
import RequestRide from "./Pages/Ride/Ride";
import { BrowserRouter, Routes, Route } from "react-router-dom";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/get-locations" element={<GetLocations />} />
        <Route path="/ride" element={<RequestRide />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
