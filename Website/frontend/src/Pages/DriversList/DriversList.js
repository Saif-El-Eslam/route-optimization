import React from "react";
import "./DriversList.css";
import Header from "../../Components/Header/Header";

const DriversList = () => {
  return (
    <div>
      <Header />
      <div className="drivers-list">
        <div className="drivers-list-title">
          <h2>Drivers List</h2>
        </div>
        <div className="drivers-list-container">
          <div className="drivers-list-header">
            <div className="header-card">
              <div className="header-item">ID</div>
              <div className="header-item">Name</div>
              <div className="header-item">Email</div>
              <div className="header-item">License Number</div>
              <div className="header-item">Verified</div>
            </div>
          </div>
          <div className="drivers-list-content">
            <div className="content-card">
              <div className="content-item">65216d8b957247b850940d69</div>
              <div className="content-item">driver test</div>
              <div className="content-item">driver@test.com</div>
              <div className="content-item">12345678909999</div>
              <div className="content-item">Yes</div>
              <div className="activate-button">Activate</div>
            </div>
            <div className="content-card">
              <div className="content-item">1</div>
              <div className="content-item">John Doe</div>
              <div className="content-item">test@mail.com</div>
              <div className="content-item">1234567890</div>
              <div className="content-item">Yes</div>
              <div className="deactivate-button">Deactivate</div>
            </div>
            <div className="content-card">
              <div className="content-item">1</div>
              <div className="content-item">John Doe</div>
              <div className="content-item">test@mail.com</div>
              <div className="content-item">1234567890</div>
              <div className="content-item">Yes</div>
            </div>
            <div className="content-card">
              <div className="content-item">1</div>
              <div className="content-item">John Doe</div>
              <div className="content-item">test@mail.com</div>
              <div className="content-item">1234567890</div>
              <div className="content-item">Yes</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DriversList;
