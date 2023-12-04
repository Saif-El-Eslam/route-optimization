import axios from "axios";

export const signUp = async (userType, formData) => {
  const user = {
    first_name: formData.firstName,
    last_name: formData.lastName,
    email: formData.email,
    password: formData.password,
    confirm_password: formData.confirmPassword,
    role: userType === "driver" ? 1 : 0,
  };

  if (userType === "driver") {
    user.bus_id = formData.busId;
    user.license_number = formData.licenseNumber;
  }

  return axios.post(`${process.env.REACT_APP_API_URL}/signup`, user);
};

export const login = async (formData) => {
  const user = {
    email: formData.email,
    password: formData.password,
  };

  return axios.post(`${process.env.REACT_APP_API_URL}/login`, user);
};

export const logout = async () => {
  return axios.post(
    `${process.env.REACT_APP_API_URL}/logout`,
    {},
    {
      headers: {
        Authorization: `Bearer ${
          JSON.parse(sessionStorage.getItem("user")).token
        }`,
      },
    }
  );
};
