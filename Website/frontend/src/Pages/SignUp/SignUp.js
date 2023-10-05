// SignUp.js

import React, { useState } from "react";
import "./SignUp.css";
import Header from "../../Components/Header/Header";

const SignUp = () => {
  const [userType, setUserType] = useState("rider");
  const [formData, setFormData] = useState({
    firstName: "",
    lastName: "",
    email: "",
    password: "",
    busNumber: "",
    plateNumber: "",
  });

  const handleUserTypeChange = (event) => {
    setUserType(event.target.value);
  };

  const handleInputChange = (event) => {
    const { name, value } = event.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    // You can access the selected user type and form data here.
    console.log("Selected User Type:", userType);
    console.log("Form Data:", formData);
    // Implement your sign-up logic here.
  };

  return (
    <div className="signup-page">
      <Header />
      <div className={`signup-container ${userType}`}>
        <h2>Sign Up</h2>
        <form onSubmit={handleSubmit}>
          <div className="radio-group">
            <label>
              <input
                type="radio"
                value="rider"
                checked={userType === "rider"}
                onChange={handleUserTypeChange}
              />
              Rider
            </label>
            <label>
              <input
                type="radio"
                value="driver"
                checked={userType === "driver"}
                onChange={handleUserTypeChange}
              />
              Driver
            </label>
          </div>
          <div className="form-fields">
            <input
              type="text"
              name="firstName"
              placeholder="First Name"
              value={formData.firstName}
              onChange={handleInputChange}
              required
            />
            <input
              type="text"
              name="lastName"
              placeholder="Last Name"
              value={formData.lastName}
              onChange={handleInputChange}
              required
            />
            <input
              type="email"
              name="email"
              placeholder="Email"
              value={formData.email}
              onChange={handleInputChange}
              required
            />
            <input
              type="password"
              name="password"
              placeholder="Password"
              value={formData.password}
              onChange={handleInputChange}
              required
            />
            {userType === "driver" && (
              <>
                <input
                  type="text"
                  name="busNumber"
                  placeholder="Bus Number"
                  value={formData.busNumber}
                  onChange={handleInputChange}
                  required
                />
                <input
                  type="text"
                  name="plateNumber"
                  placeholder="Plate Number"
                  value={formData.plateNumber}
                  onChange={handleInputChange}
                  required
                />
              </>
            )}
            <button type="submit">Sign Up</button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default SignUp;
