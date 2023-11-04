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

  useEffect(() => {
    setPickupPath(JSON.parse(sessionStorage.getItem("ride")).pathToPickup);
    const pickupcoordinates = pickupPath[pickupPath.length - 1];

    setDropoffPath(JSON.parse(sessionStorage.getItem("ride")).pathToDropoff);
    const dropoffCoordinates = dropoffPath[dropoffPath.length - 1];

    setRideInfo({
      pickupLocation: {
        address: JSON.parse(sessionStorage.getItem("ride")).pickupAddress,
        coordinates: pickupcoordinates,
      },
      dropoffLocation: {
        address: JSON.parse(sessionStorage.getItem("ride")).dropoffAddress,
        coordinates: dropoffCoordinates,
      },
      time: getDiffHours(
        extractTime(JSON.parse(sessionStorage.getItem("ride")).pickupTime).time,
        extractTime(JSON.parse(sessionStorage.getItem("ride")).dropoffTime).time
      ),
      // passengerCount: 1,
    });
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  useEffect(() => {
    setWholePath([...pickupPath, ...dropoffPath]);
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
                  <div className="ride-info-item-header">Pickup Location</div>
                  <div className="ride-info-item-content">
                    <div className="ride-info-item-content-address">
                      {rideInfo?.pickupLocation?.address}
                    </div>
                    {/* <div className="ride-info-item-content-city">City, State</div> */}
                  </div>
                </div>
                <div className="ride-info-item">
                  <div className="ride-info-item-header">Dropoff Location</div>
                  <div className="ride-info-item-content">
                    <div className="ride-info-item-content-address">
                      {rideInfo?.dropoffLocation?.address}
                    </div>
                    {/* <div className="ride-info-item-content-city">City, State</div> */}
                  </div>
                </div>
                <div className="ride-info-item">
                  <div className="ride-info-item-header">Time to arrive</div>
                  <div className="ride-info-item-content">{rideInfo?.time}</div>
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
            {wholePath.length !== 0 && (
              <Map
                locationCoordinates={wholePath}
                markersIndexes={[
                  0,
                  pickupPath.length - 1,
                  wholePath.length - 1,
                ]}
                openInfo={openInfo}
              />
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

const extractTime = (fullDate) => {
  // split time into array of strings by space
  const timeArray = fullDate.split(" ");
  const dayString = timeArray[0];
  const date = timeArray[1] + " " + timeArray[2]; //+ " " + timeArray[3];
  const time = timeArray[4];
  const region = timeArray[5];

  return { dayString, date, time, region };
};

const getDiffHours = (time1, time2) => {
  const time1Array = time1.split(":");
  const time2Array = time2.split(":");
  const time1Hours = parseInt(time1Array[0]);
  const time2Hours = parseInt(time2Array[0]);
  const time1Minutes = parseInt(time1Array[1]);
  const time2Minutes = parseInt(time2Array[1]);

  let diffHours = time2Hours - time1Hours;
  let diffMinutes = time2Minutes - time1Minutes;

  if (diffMinutes < 0) {
    diffHours--;
    diffMinutes += 60;
  }

  if (diffHours < 0) {
    diffHours += 24;
  }

  return diffHours + " hours " + diffMinutes + " minutes";
};

export default RequestRide;
