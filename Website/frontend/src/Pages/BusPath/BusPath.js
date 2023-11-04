import React, { useEffect } from "react";
import "./BusPath.css";
import Header from "../../Components/Header/Header";
import { useState } from "react";
import { verifyBus, getMyBus } from "../../APIFunctions/driverCalls";

const BusPath = () => {
  const [errors, setErrors] = useState([]);
  const [openInfo, setOpenInfo] = useState(true);
  const [busInfo, setBusInfo] = useState({
    bus_id: "",
    capacity: "",
    status: "",
  });

  useEffect(() => {
    getMyBus()
      .then((response) => {
        if (response.status === 200) {
          setBusInfo({
            bus_id: response.data.bus_id,
            capacity: response.data.capacity,
            status: response.data.status,
          });
          console.log(response.data);
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
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

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
                      Location Name
                    </div>
                  </div>
                  <div className="bus-ride-info-content-item">
                    <div className="bus-ride-info-content-item-title">
                      Next Customer
                    </div>
                    <div className="bus-ride-info-content-item-content">
                      Customer Name
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
                      Bus Capacity
                    </div>
                    <div className="bus-info-card-content-item-content">
                      {busInfo.capacity}
                    </div>
                  </div>
                  <div className="bus-info-card-content-item">
                    <div className="bus-info-card-content-item-title">
                      Bus Status
                    </div>
                    <div className="bus-info-card-content-item-content">
                      {busInfo.status}
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
                    ? "Deacivate"
                    : "Activate"}
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
        <div className="bus-path-map">
          {!openInfo && (
            <div className="open-info-icon button-icon">
              <img
                src="/open-menu.png"
                alt="info"
                onClick={() => setOpenInfo(!openInfo)}
              />
            </div>
          )}
          <div className={openInfo ? "dont-display" : "bus-path-map-container"}>
            Map Here
          </div>
        </div>
      </div>
    </div>
  );
};

export default BusPath;
