import React, { useEffect } from "react";
import "./BusPath.css";
import Header from "../../Components/Header/Header";
import { useState } from "react";
import {
  verifyBus,
  // getMyBus,
  getCustomerNameByTripId,
  getBusRoute,
  updateBusCurrentLocation,
} from "../../APIFunctions/driverCalls";
import { getAddress } from "../../APIFunctions/helperCalls";
import Map from "../../Components/Map/map";

const BusPath = () => {
  const [errors, setErrors] = useState([]);
  const [openInfo, setOpenInfo] = useState(true);
  const [busInfo, setBusInfo] = useState({
    bus_id: "",
    capacity: "",
    status: "",
  });
  const [rideInfo, setRideInfo] = useState({
    distance: null,
    duration: null,
  });
  const [pathPoints, setPathPoints] = useState([]);
  const [markersPoints, setMarkersPoints] = useState([]);
  const [nextLocation, setNextLocation] = useState({
    coordinates: [],
    address: "",
  });
  const [nextCustomer, setNextCustomer] = useState();
  const [currentLocation, setCurrentLocation] = useState({
    coordinates: [],
    address: "",
  });

  const [mapKey, setMapKey] = useState(0); // State variable to trigger map refresh

  const updateCurrentLocation = () => {
    navigator.geolocation.getCurrentPosition((position) => {
      updateBusCurrentLocation(
        // TODO: uncomment this
        position.coords.latitude,
        position.coords.longitude
        //kafr megahd
        // 30.8106,
        // 30.78311
        // kafr elzayat
        // 30.806077,
        // 30.82738
        //tanta
        // 30.790214,
        // 31.000053
        // Kom Hamada
        // 30.765816,
        // 30.687975

      )
        .then((response) => {
          if (response.status === 200) {
            console.log("updated location");
          }
          // update the current location
          setCurrentLocation({
            ...currentLocation,
            coordinates: [position.coords.latitude, position.coords.longitude],
          });
        })
        .catch((error) => {
          if (error.response) {
            setErrors([...errors, error.response.data.error]);
            setTimeout(() => {
              setErrors(
                errors.filter((error) => error !== error.response.data.error)
              );
            }, 3000);
          }
        });
    });
  };

  // TODO: Use this to update the current location of the bus (periodically)
  useEffect(() => {
    const interval = setInterval(() => {
      updateCurrentLocation();
      // refresh the page
      // window.location.reload();
      setMapKey((prevKey) => prevKey + 1);
    }, 5000);
    return () => clearInterval(interval);
  }, []); // eslint-disable-line react-hooks/exhaustive-deps


  useEffect(() => {
    getBusRoute()
      .then((response) => {
        if (response.status === 200) {
          setBusInfo({
            bus_id: response.data.bus_id,
            capacity: response.data.capacity,
            status: response.data.status,
          });
          setPathPoints(response.data.path);
          setMarkersPoints(
            response.data.locations.map((location) => location.coordinates)
          );
          setNextLocation({
            ...nextLocation,
            coordinates: response.data.locations[1].coordinates,
          });
          setRideInfo({
            ...rideInfo,
            distance: response.data.distance,
            duration: response.data.duration,
          });

          // get the name of the next customer
          getCustomerNameByTripId(response.data.locations[1].trip_id)
            .then((response) => {
              if (response.status === 200) {
                setNextCustomer(response.data.name);
              } else {
                setErrors([...errors, response.data.error]);
                setTimeout(() => {
                  setErrors(
                    errors.filter((error) => error !== response.data.error)
                  );
                }, 3000);
              }
            })
            .catch((error) => {
              if (error.response) {
                setErrors([...errors, error.response.data.error]);
                setTimeout(() => {
                  setErrors(
                    errors.filter(
                      (error) => error !== error.response.data.error
                    )
                  );
                }, 3000);
              }
            });
        }
      })
      .catch((error) => {
        if (error.response) {
          setErrors([...errors, error.response.data.error]);
          setTimeout(() => {
            setErrors(
              errors.filter((error) => error !== error.response.data.error)
            );
          }, 3000);
        }
      });
  }, [mapKey]); // eslint-disable-line react-hooks/exhaustive-deps

  useEffect(() => {
    // get the addresses of the next location and next customer
    getAddress(nextLocation.coordinates)
      .then((response) => {
        if (response.status === 200) {
          setNextLocation({
            ...nextLocation,
            address: response.data.features[0].place_name,
          });
        }
      })
      .catch((error) => {
        if (error.response) {
          setErrors([...errors, error.response.data.error]);
          setTimeout(() => {
            setErrors(
              errors.filter((error) => error !== error.response.data.error)
            );
          }, 3000);
        }
      });
  }, [nextLocation.coordinates]); // eslint-disable-line react-hooks/exhaustive-deps

  const handleActivateBus = () => {
    verifyBus(busInfo.status.toLowerCase() === "active" ? "inactive" : "active")
      .then((response) => {
        if (response.status === 200) {
          setBusInfo({
            ...busInfo,
            status: response.data.status,
          });
        }
      })
      .catch((error) => {
        if (error.response) {
          setErrors([...errors, error.response.data.error]);
          setTimeout(() => {
            setErrors(
              errors.filter((error) => error !== error.response.data.error)
            );
          }, 3000);
        }
      });
  };

  return (
    <div>
      <Header />
      <div className="bus-path-container">
        {openInfo && (
          <div className="bus-path-info">
            <div className="close-info-icon button-icon">
              <img
                src="/close-button.png"
                alt="close info"
                onClick={() => setOpenInfo(!openInfo)}
              />
            </div>
            <div className="bus-info-container">
              <div className="bus-ride-info">
                <div className="bus-ride-info-title">Ride Info</div>
                <div className="bus-ride-info-content">
                  <div className="bus-ride-info-content-item">
                    <div className="bus-ride-info-content-item-title">
                      Next Location
                    </div>
                    <div className="bus-ride-info-content-item-content">
                      {nextLocation.address}
                    </div>
                  </div>
                  <div className="bus-ride-info-content-item">
                    <div className="bus-ride-info-content-item-title">
                      Next Customer
                    </div>
                    <div className="bus-ride-info-content-item-content">
                      {nextCustomer}
                    </div>
                  </div>
                  <div className="bus-ride-info-content-item">
                    <div className="bus-ride-info-content-item-title">
                      Arrive in:
                    </div>
                    <div className="bus-ride-info-content-item-content">
                      {Math.round(rideInfo?.duration)} min
                      <span style={{ fontWeight: "bold" }}>
                        (~{rideInfo?.distance?.toFixed(2)} KM)
                      </span>
                    </div>
                  </div>
                </div>
              </div>

              <div className="bus-info-card">
                <div className="bus-info-card-title">Bus Info</div>
                <div className="bus-info-card-content">
                  <div className="bus-info-card-content-item">
                    <div className="bus-info-card-content-item-title">
                      Bus ID
                    </div>
                    <div className="bus-info-card-content-item-content">
                      {busInfo.bus_id}
                    </div>
                  </div>
                  <div className="bus-info-card-content-item">
                    <div className="bus-info-card-content-item-title">
                      Bus Capacity:
                    </div>
                    <div className="bus-info-card-content-item-content">
                      {busInfo?.capacity}
                    </div>
                  </div>
                  <div className="bus-info-card-content-item">
                    <div className="bus-info-card-content-item-title">
                      Bus Status:
                    </div>
                    <div className="bus-info-card-content-item-content">
                      {busInfo?.status}
                    </div>
                  </div>
                </div>
              </div>

              <div className="bus-info-button">
                <button
                  className={
                    "bus-button" +
                    (busInfo.status.toLowerCase() === "active"
                      ? " activate-bus-button"
                      : " deactivate-bus-button")
                  }
                  onClick={handleActivateBus}
                >
                  {busInfo.status.toLowerCase() === "active"
                    ? "Deacivate Bus"
                    : "Activate Bus"}
                </button>
              </div>

              <div className="bus-info-errors">
                {errors.map((error, i) => (
                  <div className="error" key={i}>
                    {error}
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
        <div className={openInfo ? "bus-path-map" : "bus-path-map-max-width"}>
          {!openInfo && (
            <div className="open-info-icon button-icon">
              <img
                src="/open-menu.png"
                alt="info"
                onClick={() => setOpenInfo(!openInfo)}
              />
            </div>
          )}
          <div
            className={!openInfo ? "dont-display" : "bus-path-map-container"}
          >
            {pathPoints.length !== 0 && markersPoints.length !== 0 && (
              <Map
                key={mapKey}
                path_points={pathPoints}
                markers_points={markersPoints}
                openInfo={openInfo}
                currentLocation={currentLocation}
              />
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default BusPath;
