import React from "react";
import "./Header.css";
import { logout } from "../../APIFunctions/authCalls";
// import Link
import { Link } from "react-router-dom";
import { useNavigate } from "react-router-dom";

const Header = () => {
  const navigate = useNavigate();
  const url = window.location.href;
  const user = JSON.parse(sessionStorage.getItem("user"));

  const handleLogout = async () => {
    const response = await logout();
    if (response.status === 200) {
      sessionStorage.removeItem("user");

      if (url.split("/")[3] !== "") navigate("/");
      window.location.reload();
    }
  };

  return (
    <div className="header-container">
      <Link to="/">
        <div className="header-title">RideShare</div>
      </Link>

      <div className="header-links">
        {user?.role === 0 && !user?.ride_id && user.ride_id === "" && (
          <Link to="/get-locations">
            <div className="header-link">Request a Ride</div>
          </Link>
        )}
        {user?.role === 0 && user?.ride_id && user.ride_id !== "" && (
          <Link to="/ride">
            <div className="header-link">My Ride</div>
          </Link>
        )}
        {user?.role === 1 && (
          <Link to="/buspath">
            <div className="header-link">Bus Path</div>
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
            <div className="header-link" onClick={handleLogout}>
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
