import axios from "axios";

export const getMyBus = async () => {
  return await axios.get("http://127.0.0.1:5000/my-bus", {
    headers: {
      Authorization: `Bearer ${
        JSON.parse(sessionStorage.getItem("user")).token
      }`,
    },
  });
};

export const verifyBus = async (verify) => {
  return await axios.post(
    "http://127.0.0.1:5000/verify-bus",
    { verify: verify },
    {
      headers: {
        Authorization: `Bearer ${
          JSON.parse(sessionStorage.getItem("user")).token
        }`,
      },
    }
  );
};

export const getBusRoute = async () => {
  return await axios.get("http://127.0.0.1:5000/bus_route", {
    headers: {
      Authorization: `Bearer ${
        JSON.parse(sessionStorage.getItem("user")).token
      }`,
    },
  });
};

export const updateBusCurrentLocation = async (lat, lng) => {
  return await axios.post(
    "http://127.0.0.1:5000/update_current_location",{
    "location": {
      "coordinates": [
          lng,
          lat
      ],
  }
  },{
    headers: {
      Authorization: `Bearer ${
        JSON.parse(sessionStorage.getItem("user")).token
      }`,
    },
  });
}



export const getCustomerNameByTripId = async (trip_id) => {
  return await axios.get(`http://127.0.0.1:5000/customer_name/${trip_id}`);
};
