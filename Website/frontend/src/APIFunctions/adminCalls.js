import axios from "axios";

export const getNotVerifiedUsers = async () => {
  return await axios.get(
    `${process.env.REACT_APP_API_URL}/not-verified-users`,
    {
      headers: {
        Authorization: `Bearer ${
          JSON.parse(sessionStorage.getItem("user")).token
        }`,
      },
    }
  );
};

export const verifyUser = async (userId, verify) => {
  return await axios.post(
    `${process.env.REACT_APP_API_URL}/verify-user`,
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
