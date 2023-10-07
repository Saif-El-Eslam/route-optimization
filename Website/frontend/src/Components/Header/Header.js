import React from "react";
import "./Header.css";

// import Link
import { Link } from "react-router-dom";
import { useNavigate } from "react-router-dom";

const Header = () => {
  const navigate = useNavigate();
  const url = window.location.href;
  const user = JSON.parse(sessionStorage.getItem("user"));

  return (
    <div className="header-container">
      <Link to="/">
        <div className="header-title">RideShare</div>
      </Link>

      <div className="header-links">
        {user?.role === 0 && (
          <Link to="/get-locations">
            <div className="header-link">Request a Ride</div>
          </Link>
        )}
        {user?.role === 2 && (
          <Link to="/drivers-list">
            <div className="header-link">Drivers' list</div>
          </Link>
        )}

        <Link to="/about">
          <div className="header-link">About</div>
        </Link>
        <Link to="/contact">
          <div className="header-link">Contact</div>
        </Link>
        {user ? (
          <Link to="/">
            <div
              className="header-link"
              onClick={() => {
                sessionStorage.removeItem("user");

                if (url.split("/")[3] === "") window.location.reload();
                else navigate("/");
              }}
            >
              Logout
            </div>
          </Link>
        ) : (
          <Link to={url.includes("/signup") ? "/" : "/signup"}>
            <div className="header-link">
              {url.includes("/signup") ? "Login" : "Sign Up"}
            </div>
          </Link>
        )}
      </div>
    </div>
  );
};

export default Header;
