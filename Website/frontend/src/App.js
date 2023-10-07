import "./App.css";
import Home from "./Pages/Home/Home";
import GetLocations from "./Pages/GetLocations/GetLocations";
import RequestRide from "./Pages/Ride/Ride";
import SignUp from "./Pages/SignUp/SignUp";
// import Login from "./Pages/Login/Login";
import NotFound from "./Pages/NotFound/NotFound";

import { BrowserRouter, Routes, Route } from "react-router-dom";

const user = JSON.parse(sessionStorage.getItem("user"));
console.log(user);

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        {user?.role === 0 && (
          <Route path="/get-locations" element={<GetLocations />} />
        )}
        {user?.role === 0 && <Route path="/ride" element={<RequestRide />} />}
        {/* <Route path="/rider/:id" element={<Rider />} />
        <Route path="/driver/:id" element={<Driver />} /> */}
        <Route path="/signup" element={<SignUp />} />
        {/* <Route path="/login" element={<Login />} /> */}

        <Route path="/*" element={<NotFound />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
