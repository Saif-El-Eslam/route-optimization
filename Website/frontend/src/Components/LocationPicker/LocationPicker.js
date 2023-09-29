import React, { useEffect, useState, useRef } from "react";
import mapboxgl from "mapbox-gl";
import MapboxGeocoder from "@mapbox/mapbox-gl-geocoder";
import "./LocationPicker.css";
import { useNavigate } from "react-router-dom";
import { reqestRide } from "../../APIFunctions/DBFunctions.js";

mapboxgl.accessToken =
  "pk.eyJ1IjoiaGFuZy1obyIsImEiOiJjbDA2M3F6bm4xcW05M2RvZHhpeDFsZTVvIn0.Ot8ZrqGcvLYWRLzyXtkUdA";

const LocationPicker = ({
  pickupLocation,
  setPickupLocation,
  dropoffLocation,
  setDropoffLocation,
}) => {
  const navigate = useNavigate();

  const [confirmed, setConfirmed] = useState(false);
  // const [response, setResponse] = useState(null);

  const pickupGeocoderRef = useRef(null);
  const dropoffGeocoderRef = useRef(null);

  useEffect(() => {
    // Create geocoders if they haven't been created yet
    if (!pickupGeocoderRef.current) {
      const pickupGeocoder = new MapboxGeocoder({
        accessToken: mapboxgl.accessToken,
        placeholder: pickupLocation || "Enter Pickup Location",
        types: "address,place,postcode,locality,neighborhood",
      });
      pickupGeocoderRef.current = pickupGeocoder;
      pickupGeocoder.addTo("#pickup-box");
      pickupGeocoder.on("result", (e) => {
        setPickupLocation(e.result.geometry.coordinates);
      });
    }

    if (!dropoffGeocoderRef.current) {
      const dropoffGeocoder = new MapboxGeocoder({
        accessToken: mapboxgl.accessToken,
        placeholder: "Enter Dropoff Location",
        types: "address,place,postcode,locality,neighborhood",
      });
      dropoffGeocoderRef.current = dropoffGeocoder;
      dropoffGeocoder.addTo("#dropoff-box");
      dropoffGeocoder.on("result", (e) => {
        setDropoffLocation(e.result.geometry.coordinates);
      });
    }

    // Fetch the user's current location using Geolocation API
    navigator.geolocation.getCurrentPosition(
      (position) => {
        const { latitude, longitude } = position.coords;
        const coordinates = [longitude, latitude]; // Reversed for Mapbox
        setPickupLocation(coordinates); // Set the current location in the pickup box
        pickupGeocoderRef.current.setPlaceholder(`Current Location`);
      },
      (error) => {
        console.error("Error fetching current location:", error);
      }
    );
  });

  const handleConfirm = async () => {
    if (pickupLocation && dropoffLocation) {
      setConfirmed(true);
      const time = new Date();
      const passengerCount = 1;
      const requestData = {
        pickupLocation: pickupLocation,
        dropoffLocation: dropoffLocation,
        requestTime: time,
        passengerCount: passengerCount,
      };
      const response = await reqestRide(requestData);
      if (response) {
        // navigate to next page
        navigate("/ride");
      }
    }
  };

  return (
    <div className="location-picker-container">
      <div className="location-picker-header">
        <div className="location-picker-header-logo">
          <img src="/car.svg" alt="logo" />
        </div>
        <div className="location-picker-header-title">Request a ride now</div>
      </div>
      <div className="search-container">
        <div id="pickup-box" className="geocoder"></div>
        <div id="dropoff-box" className="geocoder"></div>
      </div>

      <div className="location-picker-button-container">
        <button
          className="confirm"
          onClick={handleConfirm}
          disabled={confirmed}
        >
          Request now
        </button>
      </div>
    </div>
  );
};

export default LocationPicker;
