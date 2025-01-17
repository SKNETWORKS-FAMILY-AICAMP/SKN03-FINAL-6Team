import axios from "axios";

const SocialAxiosInstance = axios.create({
  baseURL: "http://54.180.117.149:8080", // 소셜 로그인 서버 URL
  timeout: 10000,
  headers: {
    "Content-Type": "application/json",
  },
});

export default SocialAxiosInstance;