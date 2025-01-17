import axios from "axios";

const axiosInstance = axios.create({
  baseURL: "http://54.180.117.149:8080", // 서버 URL
  timeout: 10000,
  headers: {
    "Content-Type": "application/json",
  },
});

axiosInstance.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("authToken");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

axiosInstance.interceptors.response.use(
  (response) => response,
  (error) => {
    const { status } = error.response || {};
    if (status === 403) {
      console.error("접근 거부: 권한 확인 필요.");
    } else if (status === 401) {
      console.error("인증 필요: 로그인 후 다시 시도하세요.");
    }
    return Promise.reject(error);
  }
);

export default axiosInstance;