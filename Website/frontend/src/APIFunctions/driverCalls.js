import axios from "axios";

export const getMyBus = async () => {
  return await axios.get(`${process.env.REACT_APP_API_URL}/my-bus`, {
    headers: {
      Authorization: `Bearer ${
        JSON.parse(sessionStorage.getItem("user")).token
      }`,
    },
  });
};

export const verifyBus = async (verify) => {
  return await axios.post(
    `${process.env.REACT_APP_API_URL}/verify-bus`,
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
  return await axios.get(`${process.env.REACT_APP_API_URL}/bus_route`, {
    headers: {
      Authorization: `Bearer ${
        JSON.parse(sessionStorage.getItem("user")).token
      }`,
    },
  });
};

export const updateBusCurrentLocation = async (lat, lng) => {
  return await axios.post(
    `${process.env.REACT_APP_API_URL}/update_current_location`,
    {
      location: {
        coordinates: [lng, lat],
      },
    },
    {
      headers: {
        Authorization: `Bearer ${
          JSON.parse(sessionStorage.getItem("user")).token
        }`,
      },
    }
  );
};

export const getCustomerNameByTripId = async (trip_id) => {
  return await axios.get(
    `${process.env.REACT_APP_API_URL}/customer_name/${trip_id}`
  );
};
