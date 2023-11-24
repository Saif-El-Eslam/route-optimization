import React, { useEffect } from "react";
import "./Ride.css";
import Header from "../../Components/Header/Header";
import { useState } from "react";
import Map from "../../Components/Map/map";
import { getRideInfo } from "../../APIFunctions/riderCalls.js";
import { getAddress } from "../../APIFunctions/helperCalls.js";

const RequestRide = () => {
  const [openInfo, setOpenInfo] = useState(true);
  const [rideInfo, setRideInfo] = useState();
  const [pickupPath, setPickupPath] = useState([]);
  const [dropoffPath, setDropoffPath] = useState([]);
  const [pickupAddress, setPickupAddress] = useState();
  const [dropoffAddress, setDropoffAddress] = useState();
  const [wholePath, setWholePath] = useState([]);
  const [markers, setMarkers] = useState([]);
  const [mapKey, setMapKey] = useState(0);
  // TODO: get the data dynamically as it not updated periodically as it shoudlbe (look at the map key useEffect for more info)
  // useEffect(() => {
  //   setPickupPath(JSON.parse(sessionStorage.getItem("ride"))?.pathToPickup);
  //   const pickupcoordinates = pickupPath[pickupPath.length - 1];

  //   setDropoffPath(JSON.parse(sessionStorage.getItem("ride"))?.pathToDropoff);
  //   const dropoffCoordinates = dropoffPath[dropoffPath.length - 1];

  //   setRideInfo({
  //     assignedBus: JSON.parse(sessionStorage.getItem("ride"))?.busId,
  //     pickupLocation: {
  //       address: JSON.parse(sessionStorage.getItem("ride"))?.pickupAddress,
  //       coordinates: pickupcoordinates,
  //     },
  //     dropoffLocation: {
  //       address: JSON.parse(sessionStorage.getItem("ride"))?.dropoffAddress,
  //       coordinates: dropoffCoordinates,
  //     },
  //     timeToPickup: JSON.parse(sessionStorage.getItem("ride"))
  //       ?.durationToPickup,
  //     timeToDropoff: JSON.parse(sessionStorage.getItem("ride"))
  //       ?.durationToDropoff,
  //     distanceToPickup: JSON.parse(sessionStorage.getItem("ride"))
  //       ?.distanceToPickup,
  //     distanceToDropoff: JSON.parse(sessionStorage.getItem("ride"))
  //       ?.distanceToDropoff,

  //     // passengerCount: 1,
  //   });
  // }, []); // eslint-disable-line react-hooks/exhaustive-deps

  // // update the map key every 10 seconds to force a re-render
  // useEffect(() => {
  //   const interval = setInterval(() => {
  //     setMapKey(mapKey + 1);
  //   }, 10000);
  //   return () => clearInterval(interval);
  // }, [mapKey]);

  // useEffect(() => {
  //   setWholePath([...pickupPath, ...dropoffPath]);
  //   setMarkers([
  //     pickupPath[0],
  //     pickupPath[pickupPath.length - 1],
  //     dropoffPath[dropoffPath.length - 1],
  //   ]);
  // }, [pickupPath, dropoffPath]);

  useEffect(() => {
    getRideInfo()
      .then((response) => {
        if (response.status === 200) {
          setRideInfo(response.data);
          // setPickupPath(response.data.pathToPickup);
          // setDropoffPath(response.data.pathToDropoff);
          // console.log(response.data);
        }
      })
      .catch((error) => {
        console.log(error);
      });
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  useEffect(() => {
    if (rideInfo?.pickup_coordinates && rideInfo?.dropoff_coordinates) {
      getAddress(rideInfo.pickup_coordinates)
        .then((response) => {
          if (response.status === 200) {
            setPickupAddress(response.data.features[0].place_name);
          }
        })
        .catch((error) => {
          console.log(error);
        });

      getAddress(rideInfo.dropoff_coordinates)
        .then((response) => {
          if (response.status === 200) {
            setDropoffAddress(response.data.features[0].place_name);
          }
        })
        .catch((error) => {
          console.log(error);
        });
    }
  }, [rideInfo]); // eslint-disable-line react-hooks/exhaustive-deps

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
                    {rideInfo?.busId}
                  </div>
                </div>

                <div className="ride-info-item">
                  <div className="ride-info-item-header">From:</div>
                  <div className="ride-info-item-content">
                    <div className="ride-info-item-content-address">
                      {pickupAddress}
                    </div>
                    {/* <div className="ride-info-item-content-city">City, State</div> */}
                  </div>
                </div>
                <div className="ride-info-item">
                  <div className="ride-info-item-header">To:</div>
                  <div className="ride-info-item-content">
                    <div className="ride-info-item-content-address">
                      {dropoffAddress}
                    </div>
                    {/* <div className="ride-info-item-content-city">City, State</div> */}
                  </div>
                </div>
                <div className="ride-info-item">
                  <div className="ride-info-item-header">Pickup in: </div>
                  <div className="ride-info-item-content">
                    {Math.round(rideInfo?.timeToPickup)} min
                    <span style={{ fontWeight: "bold" }}>
                      (~{rideInfo?.distanceToPickup?.toFixed(2)} KM)
                    </span>
                  </div>
                </div>
                <div className="ride-info-item">
                  <div className="ride-info-item-header">Arrive in: </div>
                  <div className="ride-info-item-content">
                    {Math.round(
                      rideInfo?.timeToDropoff + rideInfo?.timeToPickup
                    )}{" "}
                    min
                    <span style={{ fontWeight: "bold" }}>
                      (~{rideInfo?.distanceToDropoff?.toFixed(2)} KM)
                    </span>
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
                key={mapKey}
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
