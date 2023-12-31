import React from "react";
import "./NotFound.css";
import Header from "../../Components/Header/Header";
import { useNavigate } from "react-router-dom";

const NotFound = () => {
  const navigate = useNavigate();
  // direct to home page after 3 seconds
  setTimeout(() => {
    navigate("/");
  }, 3000);

  return (
    <div>
      <Header />
      <div className="not-found-container">
        <div className="not-found-header">404</div>
        <div className="not-found-subheader">Page Not Found</div>

        <div className="not-found-text">
          The page you are looking for does not exist or you are not authorized
          to open.
        </div>
        <div className="not-found-text">redirecting to home page...</div>
      </div>
    </div>
  );
};

export default NotFound;
