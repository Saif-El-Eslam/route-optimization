import React from "react";
import "./Home.css";
import Header from "../../Components/Header/Header";
import { login } from "../../APIFunctions/authCalls";
import { useNavigate } from "react-router-dom";
import { useState } from "react";

const Home = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });
  const [errors, setErrors] = useState([]);
  const [loggedIn, setLoggedIn] = useState(
    sessionStorage.getItem("user") ? true : false
  );

  const handleSubmit = (event) => {
    event.preventDefault();
    // Implement your log-in logic here.
    login(formData)
      .then((response) => {
        // set user in session storage
        sessionStorage.setItem("user", JSON.stringify(response.data));
        setLoggedIn(true);

        if (response.data.role === 0) navigate("/get-locations");
        else if (response.data.role === 1) navigate("/buspath");
        else if (response.data.role === 2) navigate("/drivers-list");
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
    <div className="home-container">
      <Header />
      {!loggedIn ? (
        <div className="login-container">
          <h2>Login</h2>
          <form onSubmit={handleSubmit}>
            <input
              type="text"
              placeholder="Username"
              value={formData.email}
              onChange={(event) => {
                setFormData({
                  ...formData,
                  email: event.target.value,
                });
              }}
              required
            />
            <input
              type="password"
              placeholder="Password"
              value={formData.password}
              onChange={(event) => {
                setFormData({
                  ...formData,
                  password: event.target.value,
                });
              }}
              required
            />
            {errors &&
              errors.map((error, i) => (
                <div key={i} className="error">
                  {error}
                </div>
              ))}
            <button type="submit" onClick={handleSubmit}>
              Login
            </button>
          </form>
          {/* Don't have an account ? signup */}
          <div className="signup-link">
            Don't have an account ? <a href="/signup">Sign Up</a>
          </div>
        </div>
      ) : (
        <div></div>
      )}
    </div>
  );
};

export default Home;
