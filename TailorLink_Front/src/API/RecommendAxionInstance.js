import axios from "axios";

const recommendAxiosInstance = axios.create({
  baseURL: "http://3.39.245.44:8000/", // 차량 추천 API의 Base URL
  timeout: 100000,
  headers: {
    "Content-Type": "application/json",
  },
});

recommendAxiosInstance.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error("API 호출 오류:", error);
    return Promise.reject(error);
  }
);

export default recommendAxiosInstance;