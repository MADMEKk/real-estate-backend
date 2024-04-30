import axios from "axios";

const REGISTER_URL = "http://127.0.0.1:8000/api/v1/auth/users/";
const LOGIN_URL = "http://127.0.0.1:8000/api/v1/auth/jwt/create/";
const REFRESH_URL = "http://127.0.0.1:8000/api/v1/auth/jwt/refresh/";
const VERIFY_URL = "http://127.0.0.1:8000/api/v1/auth/jwt/verify/";
const ACTIVATE_URL = "http://127.0.0.1:8000/api/v1/auth/users/activation/";

// Register user
const register = async (userData) => {
  const config = {
    headers: {
      "Content-Type": "application/json",
    },
  };
  const response = await axios.post(REGISTER_URL, userData, config);

  return response.data;
};

// Login user
const login = async (userData) => {
  const config = {
    headers: {
      "Content-Type": "application/json",
    },
  };

  const response = await axios.post(LOGIN_URL, userData, config);
  if (response.data.access) {
    localStorage.setItem("user", JSON.stringify(response.data));
  }

  return response.data;
};

// Refresh JWT token
const refresh = async () => {
  const refreshToken = JSON.parse(localStorage.getItem("user")).refresh;
  const data = { refresh: refreshToken };

  const config = {
    headers: {
      "Content-Type": "application/json",
    },
  };

  const response = await axios.post(REFRESH_URL, data, config);
  if (response.data.access) {
    const userData = JSON.parse(localStorage.getItem("user"));
    userData.access = response.data.access;
    localStorage.setItem("user", JSON.stringify(userData));
  }

  return response.data;
};

// Verify JWT token
const verifyToken = async () => {
  const token = JSON.parse(localStorage.getItem("user")).access;
  const data = { token };

  const config = {
    headers: {
      "Content-Type": "application/json",
    },
  };

  const response = await axios.post(VERIFY_URL, data, config);
  return response.data;
};

// Logout user
const logout = () => localStorage.removeItem("user");

const activate = async (userData) => {
  const config = {
    headers: {
      "Content-Type": "application/json",
    },
  };

  const response = await axios.post(ACTIVATE_URL, userData, config);
  return response.data;
};

const authService = { register, login, logout, activate, refresh, verifyToken };

export default authService;
