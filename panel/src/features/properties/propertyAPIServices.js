import axios from "axios";

// Function to get properties with JWT authentication
const getProperties = async () => {
  const token = JSON.parse(localStorage.getItem("user")).access; // Get the JWT access token from local storage
  const config = {
    headers: {
      "Authorization": `Bearer ${token}` // Include the JWT token in the request headers
    }
  };

  try {
    const response = await axios.get("http://127.0.0.1:8000/api/v1/properties/myporp", config);
    return response.data;
  } catch (error) {
    throw error; // Handle errors appropriately
  }
};

const publishProperty = async (propertyId) => {
  const token = JSON.parse(localStorage.getItem("user")).access;
  const config = {
    headers: {
      "Authorization": `Bearer ${token}`
    }
  };

  try {
    const response = await axios.put(`http://127.0.0.1:8000/api/v1/properties/toggle-publish/${propertyId}/`, { published: true }, config);
    return response.data;
  } catch (error) {
    throw error; // Handle errors appropriately
  }
};

const unpublishProperty = async (propertyId) => {
  const token = JSON.parse(localStorage.getItem("user")).access;
  const config = {
    headers: {
      "Authorization": `Bearer ${token}`
    }
  };

  try {
    const response = await axios.put(`http://127.0.0.1:8000/api/v1/properties/toggle-publish/${propertyId}/`, { published: false }, config);
    return response.data;
  } catch (error) {
    throw error; // Handle errors appropriately
  }
};

const propertyAPIService = { getProperties, publishProperty, unpublishProperty };

export default propertyAPIService;
