import mapboxgl from "mapbox-gl";
import axios from "axios";

// Include the Mapbox JavaScript library
mapboxgl.accessToken =
  "pk.eyJ1IjoiaGFuZy1obyIsImEiOiJjbDA2M3F6bm4xcW05M2RvZHhpeDFsZTVvIn0.Ot8ZrqGcvLYWRLzyXtkUdA";

export const getAddress = async (coordinates) => {
  return await axios.get(
    `https://api.mapbox.com/geocoding/v5/mapbox.places/${coordinates[0]},${coordinates[1]}.json?access_token=${mapboxgl.accessToken}`
  );
};
