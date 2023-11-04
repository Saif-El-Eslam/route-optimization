import React, { useEffect } from "react";
import "./Ride.css";
import Header from "../../Components/Header/Header";
import { useState } from "react";
import Map from "../../Components/Map/map";

const RequestRide = () => {
  const [openInfo, setOpenInfo] = useState(true);
  const [rideInfo, setRideInfo] = useState();
  const [pickupPath, setPickupPath] = useState([]);
  const [dropoffPath, setDropoffPath] = useState([]);
  const [wholePath, setWholePath] = useState([]);
  const [markers, setMarkers] = useState([]);

  useEffect(() => {
    setPickupPath(JSON.parse(sessionStorage.getItem("ride")).pathToPickup);
    const pickupcoordinates = pickupPath[pickupPath.length - 1];

    setDropoffPath(JSON.parse(sessionStorage.getItem("ride")).pathToDropoff);
    const dropoffCoordinates = dropoffPath[dropoffPath.length - 1];

    setRideInfo({
      assignedBus: JSON.parse(sessionStorage.getItem("ride")).busId,
      pickupLocation: {
        address: JSON.parse(sessionStorage.getItem("ride")).pickupAddress,
        coordinates: pickupcoordinates,
      },
      dropoffLocation: {
        address: JSON.parse(sessionStorage.getItem("ride")).dropoffAddress,
        coordinates: dropoffCoordinates,
      },
      timeToPickup: JSON.parse(sessionStorage.getItem("ride")).durationToPickup,
      timeToDropoff: JSON.parse(sessionStorage.getItem("ride"))
        .durationToDropoff,
      distanceToPickup: JSON.parse(sessionStorage.getItem("ride"))
        .distanceToPickup,
      distanceToDropoff: JSON.parse(sessionStorage.getItem("ride"))
        .distanceToDropoff,

      // passengerCount: 1,
    });
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  useEffect(() => {
    setWholePath([...pickupPath, ...dropoffPath]);
    setMarkers([
      pickupPath[0],
      pickupPath[pickupPath.length - 1],
      dropoffPath[dropoffPath.length - 1],
    ]);
  }, [pickupPath, dropoffPath]);

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
                  <div className="ride-info-item-header">Bus:</div>
                  <div className="ride-info-item-content">
                    {rideInfo?.assignedBus}
                  </div>
                </div>

                <div className="ride-info-item">
                  <div className="ride-info-item-header">From:</div>
                  <div className="ride-info-item-content">
                    <div className="ride-info-item-content-address">
                      {rideInfo?.pickupLocation?.address}
                    </div>
                    {/* <div className="ride-info-item-content-city">City, State</div> */}
                  </div>
                </div>
                <div className="ride-info-item">
                  <div className="ride-info-item-header">To:</div>
                  <div className="ride-info-item-content">
                    <div className="ride-info-item-content-address">
                      {rideInfo?.dropoffLocation?.address}
                    </div>
                    {/* <div className="ride-info-item-content-city">City, State</div> */}
                  </div>
                </div>
                <div className="ride-info-item">
                  <div className="ride-info-item-header">Pickup in: </div>
                  <div className="ride-info-item-content">
                    {Math.floor(rideInfo?.timeToPickup)} {" "}
                   min 
                  <span style={ {fontWeight: "bold"}}>(~{Math.ceil(rideInfo?.distanceToPickup)} KM)</span>
            
                  </div>
                </div>
                <div className="ride-info-item">
                  <div className="ride-info-item-header">Arrive in: </div>
                  <div className="ride-info-item-content">
                    {Math.floor(rideInfo?.timeToDropoff) +
                      Math.floor(rideInfo?.timeToPickup)}{" "}
                    min 
                    <span style={ {fontWeight: "bold"}}>(~{Math.ceil(rideInfo?.distanceToDropoff)} KM)</span>

                  </div>
                </div>

                {/* <div className="ride-info-item">
                  <div className="ride-info-item-header">Passenger Count</div>
                  <div className="ride-info-item-content">
                    {rideInfo.passengerCount}
                  </div>
                </div> */}
              </div>
            </div>
          </div>
        )}
        <div className={openInfo ? "ride-map" : "ride-map-max-width"}>
          {!openInfo && (
            <div className="open-info-icon button-icon">
              <img
                src="/open-menu.png"
                alt="info"
                onClick={() => setOpenInfo(!openInfo)}
              />
            </div>
          )}
          <div className={!openInfo ? "dont-display" : "ride-map-container"}>
            {wholePath.length !== 0 && markers.length !== 0 && (
              <Map
                path_points={wholePath}
                markers_points={markers}
                openInfo={openInfo}
              />
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default RequestRide;
