// Implemnt the calls to the backend here

export async function addUser(userData) {
  return "addUser";
}

export async function reqestRide(requestData) {
  try {
    const response = await fetch("http://localhost:5000/process_request", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(requestData),
    });
    if (!response.ok) {
      throw new Error(`HTTP Error! Status: ${response.status}`);
    }
    const responseData = await response.json();
    return responseData;
  } catch (error) {
    console.error("Error:", error);
    return null;
  }
}