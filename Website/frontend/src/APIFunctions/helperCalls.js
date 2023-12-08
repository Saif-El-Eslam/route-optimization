import mapboxgl from "mapbox-gl";
import axios from "axios";

// Include the Mapbox JavaScript library
mapboxgl.accessToken =
  "pk.eyJ1IjoiYWhtZWR5MTU1MjAwIiwiYSI6ImNscHU2anR0cjBrMjYyam1samJqN3Y5ZHcifQ.rI8SUfxadkqVpvemVZdvPw";

export const getAddress = async (coordinates) => {
  return await axios.get(
    `https://api.mapbox.com/geocoding/v5/mapbox.places/${coordinates[0]},${coordinates[1]}.json?access_token=${mapboxgl.accessToken}`
  );
};
