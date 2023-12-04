import axios from "axios";

export const getNotVerifiedUsers = async () => {
  return await axios.get("http://127.0.0.1:5000/not-verified-users", {
    headers: {
      Authorization: `Bearer ${
        JSON.parse(sessionStorage.getItem("user")).token
      }`,
    },
  });
};

export const verifyUser = async (userId, verify) => {
  return await axios.post(
    "http://127.0.0.1:5000/verify-user",
    { verify: verify, user_id: userId },
    {
      headers: {
        Authorization: `Bearer ${
          JSON.parse(sessionStorage.getItem("user")).token
        }`,
      },
    }
  );
};
