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
