import "./App.css";
import Home from "./Pages/Home/Home";
import GetLocations from "./Pages/GetLocations/GetLocations";
import RequestRide from "./Pages/Ride/Ride";
import SignUp from "./Pages/SignUp/SignUp";
// import Login from "./Pages/Login/Login";
import NotFound from "./Pages/NotFound/NotFound";
import Loading from "./Pages/NotFound/Loading";
import Contact from "./Pages/Contact/Contact";
import About from "./Pages/About/About";
import DriversList from "./Pages/DriversList/DriversList";
import BusPath from "./Pages/BusPath/BusPath";

import { BrowserRouter, Routes, Route } from "react-router-dom";

const user = JSON.parse(sessionStorage.getItem("user"));

// add urls to the session storage
sessionStorage.setItem(
  "urls",
  JSON.stringify([
    "",
    "get-locations",
    "ride",
    "signup",
    "contact",
    "about",
    "not-found",
    "*",
    "drivers-list",
    "buspath",
  ])
);

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        {user?.role === 0 && !user?.ride_id && user?.ride_id === "" && (
          <Route path="/get-locations" element={<GetLocations />} />
        )}
        {user?.role === 0 && user?.ride_id && user?.ride_id !== "" && (
          <Route path="/ride" element={<RequestRide />} />
        )}
        {user?.role === 1 && <Route path="/buspath" element={<BusPath />} />}
        {user?.role === 2 && (
          <Route path="/drivers-list" element={<DriversList />} />
        )}
        {/* <Route path="/rider/:id" element={<Rider />} />
        <Route path="/driver/:id" element={<Driver />} /> */}
        <Route path="/signup" element={<SignUp />} />
        {/* <Route path="/login" element={<Login />} /> */}

        <Route path="/contact" element={<Contact />} />
        <Route path="/about" element={<About />} />

        <Route path="/not-found" element={<NotFound />} />
        <Route path="/*" element={<Loading />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
