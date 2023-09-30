import React from "react";
import "./Ride.css";
import Header from "../../Components/Header/Header";
import { getRide } from "../../ReduxStore/actions";
import { useState } from "react";

const RequestRide = () => {
  const [rideInfo, setRideInfo] = useState(getRide());

  console.log(rideInfo);

  return (
    <div>
      <Header />
      <div className="ride-container">
        <div className="ride-info-container">
          <div className="ride-info-header">Ride Info</div>
          <div className="ride-info">
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
        <div className="ride-map-container">map</div>
      </div>
    </div>
  );
};

export default RequestRide;
