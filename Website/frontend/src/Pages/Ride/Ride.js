import React from "react";
import "./Ride.css";
import Header from "../../Components/Header/Header";
import { useState } from "react";

const RequestRide = () => {
  const [openInfo, setOpenInfo] = useState(true);
  const [rideInfo, setRideInfo] = useState({
    pickupLocation: {
      address: "123 Main St San Diego CA",
      coordinates: [-117.161084, 32.715736],
    },
    dropoffLocation: {
      address: "456 Main St San Diego CA",
      coordinates: [-117.161084, 32.715736],
    },
    time: "ASAP",
    passengerCount: 1,
  });

  console.log(rideInfo);

  return (
    <div>
      <Header />
      <div className="ride-container">
        {openInfo && (
          <div className="ride-info">
            <div className="close-info-icon button-icon">
              <img
                src="/close-button.png"
                alt="close info"
                onClick={() => setOpenInfo(!openInfo)}
              />
            </div>
            <div className="ride-info-container">
              <div className="ride-info-header">Ride Info</div>
              <div className="ride-info-content">
                <div className="ride-info-item">
                  <div className="ride-info-item-header">Pickup Location</div>
                  <div className="ride-info-item-content">
                    <div className="ride-info-item-content-address">
                      {rideInfo.pickupLocation.address}
                    </div>
                    {/* <div className="ride-info-item-content-city">City, State</div> */}
                  </div>
                </div>
                <div className="ride-info-item">
                  <div className="ride-info-item-header">Dropoff Location</div>
                  <div className="ride-info-item-content">
                    <div className="ride-info-item-content-address">
                      {rideInfo.dropoffLocation.address}
                    </div>
                    {/* <div className="ride-info-item-content-city">City, State</div> */}
                  </div>
                </div>
                <div className="ride-info-item">
                  <div className="ride-info-item-header">Time</div>
                  <div className="ride-info-item-content">{rideInfo.time}</div>
                </div>
                <div className="ride-info-item">
                  <div className="ride-info-item-header">Passenger Count</div>
                  <div className="ride-info-item-content">
                    {rideInfo.passengerCount}
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
        <div className={openInfo ? "dont-display" : "ride-map"}>
          {!openInfo && (
            <div className="open-info-icon button-icon">
              <img
                src="/open-menu.png"
                alt="info"
                onClick={() => setOpenInfo(!openInfo)}
              />
            </div>
          )}
          <div className="ride-map-container">Map Here</div>
        </div>
      </div>
    </div>
  );
};

export default RequestRide;
