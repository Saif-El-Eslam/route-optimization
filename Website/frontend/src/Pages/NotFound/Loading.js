import React from "react";
import "./NotFound.css";
import Header from "../../Components/Header/Header";

const Loading = () => {
  const urls = JSON.parse(sessionStorage.getItem("urls"));
  const currentUrl = window.location.href.split("/").pop();

  if (urls.includes(currentUrl)) {
    window.location.reload();
  } else {
    window.location.href = "/not-found";
  }

  return (
    <div>
      <Header />
      <div className="loading">
        <h1>Loading...</h1>
      </div>
    </div>
  );
};

export default Loading;
