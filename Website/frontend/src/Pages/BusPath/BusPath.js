import React from "react";
import "./BusPath.css";
import Header from "../../Components/Header/Header";
import { useState } from "react";

const BusPath = () => {
  const [openInfo, setOpenInfo] = useState(true);

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
            <div className="bus-info-wrapper">Info Here</div>
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
