import React from "react";
import "./map.css";
import { useEffect, useState } from "react";
import mapboxgl from "mapbox-gl";
import "mapbox-gl/dist/mapbox-gl.css";
mapboxgl.accessToken =
  "pk.eyJ1IjoiaGFuZy1obyIsImEiOiJjbDA2M3F6bm4xcW05M2RvZHhpeDFsZTVvIn0.Ot8ZrqGcvLYWRLzyXtkUdA";

// locationCoordinates (2D array) is an array of longitude and latitude of the addresses passed from confirm.js
const Map = ({ path_points, markers_points, openInfo }) => {
  // coordinates (2D array) stores the longitude and latitude of all the roads to connect the locations on map
  const [coordinates, setCoordinates] = useState([]);
  const [markers, setMarkers] = useState([]);
  const [mainMap, setMainMap] = useState();

  // Need this seperate useEffect for map to handle "findElementById" error
  useEffect(() => {
    const map = new mapboxgl.Map({
      container: "map",
      style: "mapbox://styles/mapbox/streets-v11",
      center: path_points[0],
      zoom: 12,
    });
    // Add control tool on map
    map.addControl(new mapboxgl.NavigationControl());
    map.addControl(
      new mapboxgl.GeolocateControl({
        positionOptions: {
          enableHighAccuracy: true,
        },
        trackUserLocation: true,
        showUserHeading: true,
      })
    );

    setMainMap(map);
  }, [openInfo]); // eslint-disable-line react-hooks/exhaustive-deps

  // Main useEffect to fetch data (long and lat) from MapBox
  // Add marker on map
  // add different color for first location of the coordinates
  const addToMap = (map, markers) => {
    new mapboxgl.Marker().setLngLat(markers).addTo(map);
  };

  useEffect(() => {
    // If there is prop passed down from parent
    if (path_points && markers_points) {
      setCoordinates(path_points);
      setMarkers(markers_points);
    }
  }, [coordinates, mainMap, path_points]); // eslint-disable-line react-hooks/exhaustive-deps

  // draw markers on map
  useEffect(() => {
    if (markers.length !== 0) {
      // add different color for first location of the coordinates
      markers.forEach((marker, index) => {
        if (index === 0) {
          //create custom marker
          const el = document.createElement("div");
          el.className = "marker";
          new mapboxgl.Marker(el).setLngLat(marker).addTo(mainMap);
          
        } else {
          addToMap(mainMap, marker);
        }
      });
    }
  }, [markers, mainMap]);

  // This useEffect for drawing path line
  useEffect(() => {
    if (coordinates.length !== 0) {
      // console.log(coordinates);
      // Zoom out on map
      mainMap.fitBounds([path_points[0], path_points[path_points.length - 1]], {
        padding: 150,
      });
      // Draw path line on map
      mainMap.on("load", () => {
        mainMap.addSource("route", {
          type: "geojson",
          data: {
            type: "Feature",
            properties: {},
            geometry: {
              type: "LineString",
              coordinates: coordinates,
            },
          },
        });
        mainMap.addLayer({
          id: "route",
          type: "line",
          source: "route",
          layout: {
            "line-join": "round",
            "line-cap": "round",
          },
          paint: {
            "line-color": "#12113D",
            "line-width": 4,
          },
        });
      });
    }
  }, [coordinates, mainMap, path_points]);

  return <div id="map"></div>;
};

export default Map;
