import axios from "axios";
import BASEURL from "./config";

const defaultOptions = {
  baseURL: BASEURL,
  headers: {
    "Content-Type": "application/json",
  },
};

let api = axios.create(defaultOptions);
api.interceptors.request.use(function (config) {
  const user = JSON.parse(localStorage.getItem("user"));
  config.headers.Authorization = user ? `Bearer ${user.token}` : "";
  return config;
});

export default api;
