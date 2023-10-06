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
    user.bus_number = formData.busNumber;
    user.plate_number = formData.plateNumber;
  }

  axios
    .post("http://127.0.0.1:5000/signup", user)
    .then((res) => {
      console.log(res);
      return res;
    })
    .catch((error) => {
      console.log(error);
      return error;
    });
};
