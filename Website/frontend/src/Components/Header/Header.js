import React from "react";
import "./Header.css";

// import Link
import { Link } from "react-router-dom";

const Header = () => {
  const url = window.location.href;

  return (
    <div className="header-container">
      <Link to="/">
        <div className="header-title">RideShare</div>
      </Link>

      <div className="header-links">
        <Link to="/get-locations">
          <div className="header-link">Request a Ride</div>
        </Link>
        <Link to="/about">
          <div className="header-link">About</div>
        </Link>
        <Link to="/contact">
          <div className="header-link">Contact</div>
        </Link>
        <Link to={url.includes("/signup") ? "/" : "/signup"}>
          <div className="header-link">
            {url.includes("/signup") ? "Login" : "Sign Up"}
          </div>
        </Link>
      </div>
    </div>
  );
};

export default Header;
