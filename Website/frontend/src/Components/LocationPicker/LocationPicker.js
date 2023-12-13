import React, { useEffect, useState, useRef } from "react";
import mapboxgl from "mapbox-gl";
import MapboxGeocoder from "@mapbox/mapbox-gl-geocoder";
import "./LocationPicker.css";
import { useNavigate } from "react-router-dom";
import { reqestRide } from "../../APIFunctions/riderCalls.js";

mapboxgl.accessToken =
  "pk.eyJ1IjoiYWhtZWR5MTU1MjAwIiwiYSI6ImNscHU2anR0cjBrMjYyam1samJqN3Y5ZHcifQ.rI8SUfxadkqVpvemVZdvPw";

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
        setPickupLocation({
          coordinates: e.result.geometry.coordinates,
          address: e.result.place_name,
        });
        document.getElementById('dropoff-box').style.visibility = 'visible';
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
        setDropoffLocation({
          coordinates: e.result.geometry.coordinates,
          address: e.result.place_name,
        });
      });
    }

    // Fetch the user's current location using Geolocation API
    if (!pickupLocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const { latitude, longitude } = position.coords;
          const coordinates = [longitude, latitude]; // Reversed for Mapbox
          setPickupLocation({
            coordinates: coordinates,
            address: "Current Location",
          }); // Set the current location in the pickup box
          pickupGeocoderRef.current.setPlaceholder(`Current Location`);
        },
        (error) => {
          console.error("Error fetching current location:", error);
        }
      );
    }

    const handleInput = () => {
      setTimeout(() => {
        const pickupSuggestions = document.querySelector('#pickup-box .mapboxgl-ctrl-geocoder .suggestions');

        if (pickupSuggestions && window.getComputedStyle(pickupSuggestions).display === 'block') {
          // Suggestions are visible in pickup input
          // Hide dropoff input
          // document.getElementById('dropoff-box').style.display = 'none';
          document.getElementById('dropoff-box').style.visibility = 'hidden';

        } else {
          // Suggestions are not visible in pickup input
          // Show dropoff input
          // document.getElementById('dropoff-box').style.display = 'block';
          document.getElementById('dropoff-box').style.visibility = 'visible';

        }
      }, 300);
    };
    document.getElementById('pickup-box').addEventListener('input', handleInput);

    return () => {
      document.getElementById('pickup-box').removeEventListener('input', handleInput);
    };
  }, [pickupLocation, setPickupLocation]);




  const handleConfirm = async () => {
    if (pickupLocation && dropoffLocation) {
      setConfirmed(true);
      const passengerCount = 1;
      const token = JSON.parse(sessionStorage.getItem("user")).token;
      const requestData = {
        userToken: token,
        pickupLocation: pickupLocation,
        dropoffLocation: dropoffLocation,
        passengerCount: passengerCount,
      };
      const response = await reqestRide(requestData);
      if (response) {
        // add ride id to session storage
        const ride = response;
        ride.pickupAddress = pickupLocation.address;
        ride.dropoffAddress = dropoffLocation.address;

        const user = JSON.parse(sessionStorage.getItem("user"));
        user.ride_id = response.tripId;

        sessionStorage.setItem("ride", JSON.stringify(ride));
        sessionStorage.setItem("user", JSON.stringify(user));

        navigate("/ride");
      } else {
        setConfirmed(false);
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
