import React from "react";
import "./GetLocations.css";
import Header from "../../Components/Header/Header";
import LocationPicker from "../../Components/LocationPicker/LocationPicker";
import { useState } from "react";

const GetLocations = () => {
  const [pickupLocation, setPickupLocation] = useState("");
  const [dropoffLocation, setDropoffLocation] = useState("");

  return (
    <div>
      <Header />
      <div className="get-location-container">
        <LocationPicker
          pickupLocation={pickupLocation}
          setPickupLocation={setPickupLocation}
          dropoffLocation={dropoffLocation}
          setDropoffLocation={setDropoffLocation}
        />
      </div>
    </div>
  );
};

export default GetLocations;
