// SignUp.js

import React, { useState } from "react";
import "./SignUp.css";
import Header from "../../Components/Header/Header";
import { signUp } from "../../APIFunctions/authCalls";
import { useNavigate } from "react-router-dom";

const SignUp = () => {
  const navigate = useNavigate();

  const [userType, setUserType] = useState("rider");
  const [formData, setFormData] = useState({
    firstName: "",
    lastName: "",
    email: "",
    password: "",
    confirmPassword: "",
    busNumber: "",
    licenseNumber: "",
  });
  const [errors, setErrors] = useState([]);

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

    if (formData.password !== formData.confirmPassword) {
      // add password match error for 2 seconds and then remove it
      setErrors([...errors, "Passwords do not match"]);
      setTimeout(() => {
        setErrors(errors.filter((error) => error !== "Passwords do not match"));
      }, 3000);
      return;
    }

    signUp(userType, formData)
      .then((response) => {
        navigate("/");
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
            <input
              type="password"
              name="confirmPassword"
              placeholder="Confirm Password"
              value={formData.confirmPassword}
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
                  name="licenseNumber"
                  placeholder="License Number"
                  value={formData.licenseNumber}
                  onChange={handleInputChange}
                  required
                />
              </>
            )}
            {errors &&
              errors.map((error, i) => (
                <div key={i} className="error">
                  {error}
                </div>
              ))}
            <button style={{ marginTop: "2px" }} type="submit">
              Sign Up
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default SignUp;
