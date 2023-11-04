import React from "react";
import "./map.css";
import { useEffect, useState } from "react";
import mapboxgl from "mapbox-gl";
import "mapbox-gl/dist/mapbox-gl.css";
mapboxgl.accessToken =
  "pk.eyJ1IjoiaGFuZy1obyIsImEiOiJjbDA2M3F6bm4xcW05M2RvZHhpeDFsZTVvIn0.Ot8ZrqGcvLYWRLzyXtkUdA";

// locationCoordinates (2D array) is an array of longitude and latitude of the addresses passed from confirm.js
const Map = ({ locationCoordinates, markersIndexes, openInfo }) => {
  // coordinates (2D array) stores the longitude and latitude of all the roads to connect the locations on map
  const [coordinates, setCoordinates] = useState([]);
  const [mainMap, setMainMap] = useState();

  // Need this seperate useEffect for map to handle "findElementById" error
  useEffect(() => {
    const map = new mapboxgl.Map({
      container: "map",
      style: "mapbox://styles/mapbox/streets-v11",
      center: locationCoordinates[0],
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
  const addToMap = (map, coordinates) => {
    new mapboxgl.Marker().setLngLat(coordinates).addTo(map);
  };
  useEffect(() => {
    // If there is prop passed down from parent
    if (locationCoordinates && mainMap) {
      // Get the string value of all location to find all corresponding longitude and latitude
      let locationURL = "";
      locationCoordinates.map((location, i) => {
        if (markersIndexes.includes(i)) {
          addToMap(mainMap, location);
        }

        locationURL = locationURL + location[0] + "," + location[1] + ";";
        return locationURL;
      });
      locationURL = locationURL.slice(0, -1);

      locationURL &&
        fetch(
          `https://api.mapbox.com/directions/v5/mapbox/driving/${locationURL}?geometries=geojson&steps=true&access_token=pk.eyJ1IjoiaGFuZy1obyIsImEiOiJjbDA2M3F6bm4xcW05M2RvZHhpeDFsZTVvIn0.Ot8ZrqGcvLYWRLzyXtkUdA`
        )
          .then((res) => res.json())
          .then((data) => {
            // this return 2D array of all the road coordinates
            if (coordinates.length === 0) {
              setCoordinates(data.routes[0].geometry.coordinates);
            }
          });
    }
  }, [coordinates, mainMap, locationCoordinates]); // eslint-disable-line react-hooks/exhaustive-deps

  // This useEffect for drawing path line
  useEffect(() => {
    if (coordinates.length !== 0) {
      // console.log(coordinates);
      // Zoom out on map
      mainMap.fitBounds(
        [
          locationCoordinates[0],
          locationCoordinates[locationCoordinates.length - 1],
        ],
        { padding: 150 }
      );
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
            "line-width": 3,
          },
        });
      });
    }
  }, [coordinates, mainMap, locationCoordinates]);

  return <div id="map"></div>;
};

export default Map;
