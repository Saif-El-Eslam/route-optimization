import React from "react";
import "./map.css";
import { useEffect, useState, useMemo } from "react";
import mapboxgl from "mapbox-gl";
import "mapbox-gl/dist/mapbox-gl.css";
mapboxgl.accessToken =
  "pk.eyJ1IjoiaGFuZy1obyIsImEiOiJjbDA2M3F6bm4xcW05M2RvZHhpeDFsZTVvIn0.Ot8ZrqGcvLYWRLzyXtkUdA";

// locationCoordinates (2D array) is an array of longitude and latitude of the addresses passed from confirm.js
const Map = ({ locationCoordinates }) => {
  // coordinates (2D array) stores the longitude and latitude of all the roads to connect the locations on map
  const [coordinates, setCoordinates] = useState([]);
  const [mainMap, setMainMap] = useState();
  const [mapLoaded, setMapLoaded] = useState();

  // Need this seperate useEffect for map to handle "findElementById" error
  useEffect(() => {
    const map = new mapboxgl.Map({
      container: "map",
      style: "mapbox://styles/mapbox/streets-v11",
      center: locationCoordinates[0],
      zoom: 12,
    });
    // setMainMap(map);
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  return <div id="map"></div>;
};

export default Map;
