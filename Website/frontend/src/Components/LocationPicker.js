import React, { useEffect, useState, useRef } from "react";
import mapboxgl from "mapbox-gl";
import MapboxGeocoder from "@mapbox/mapbox-gl-geocoder";
import "./LocationPicker.css";

mapboxgl.accessToken =
  "pk.eyJ1IjoiaGFuZy1obyIsImEiOiJjbDA2M3F6bm4xcW05M2RvZHhpeDFsZTVvIn0.Ot8ZrqGcvLYWRLzyXtkUdA";

const LocationPicker = () => {
  const [pickupLocation, setPickupLocation] = useState("");
  const [dropoffLocation, setDropoffLocation] = useState("");
  const [confirmed, setConfirmed] = useState(false);
  const [response, setResponse] = useState(null);

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
  }, []);

  const handleConfirm = async () => {
    if (pickupLocation && dropoffLocation) {
      setConfirmed(true);
      // body: { pickupLocation, dropoffLocation , time, passenger count}
      const requestTime = new Date()
        .toISOString()
        .slice(0, 19)
        .replace("T", " ");

      const passengerCount = 1;
      const requestData = {
        requestTime: requestTime,
        pickupLocation: pickupLocation,
        dropoffLocation: dropoffLocation,
        passengerCount: passengerCount,
      };
      console.log(requestData);
      try {
        const response = await fetch("http://localhost:5000/process_request", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(requestData),
        });

        if (!response.ok) {
          throw new Error(`HTTP Error! Status: ${response.status}`);
        }

        const responseData = await response.json();
        setResponse(responseData);
        console.log(responseData);
      } catch (error) {
        console.error("Error:", error);
      }
    }
  };

  return (
    <div className="location-picker-container">
      <div className="search-container">
        <div id="pickup-box" className="geocoder"></div>
        <div id="dropoff-box" className="geocoder"></div>
        <div className="results">
          <pre>
            {confirmed
              ? `Pickup: ${pickupLocation}\nDropoff: ${dropoffLocation}`
              : ""}
          </pre>
        </div>
        <button
          className="confirm"
          onClick={handleConfirm}
          disabled={confirmed}
        >
          Confirm Locations
        </button>
      </div>
    </div>
  );
};

export default LocationPicker;
