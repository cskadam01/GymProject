import axios from "axios";

const instance = axios.create({
  baseURL:
    import.meta.env.MODE === "development"
      ? "http://localhost:8000"
      : "https://gymproject-gpdz.onrender.com",
  headers: {
    "Content-Type": "application/json",
  },
});

instance.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("access_token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

export default instance;