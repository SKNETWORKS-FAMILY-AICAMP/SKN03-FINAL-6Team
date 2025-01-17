import React, { useState, useContext } from "react";
import { useNavigate, Link } from "react-router-dom";
import axiosInstance from "../../API/AxiosInstance"; // 기본 API
import SocialAxiosInstance from "../../API/SocialAxiosInstance"; // 소셜 API
import logoImage from "../../assets/images/MainLogo.png";
import kakaoIcon from "../../assets/images/kakao.png";
import { AuthContext } from "../../API/AuthContext";
import "./Login.css";

const Login = () => {
  const [id, setId] = useState("");
  const [password, setPassword] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const { setIsLoggedIn } = useContext(AuthContext);
  const navigate = useNavigate();

  // 기본 로그인 처리
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axiosInstance.post("/v1/auth/sign-in", {
        id,
        password,
      });
      const { token } = response.data;

      // 토큰 저장
      localStorage.setItem("authToken", token);

      setIsLoggedIn(true);
      alert("로그인 되었습니다.");
      navigate("/");
    } catch (error) {
      const errorMsg =
        error.response?.data?.message || "로그인에 실패했습니다. 아이디와 비밀번호를 확인해주세요.";
      setErrorMessage(errorMsg);
      console.error("로그인 실패:", error.response?.data || error.message);
    }
  };

  // 카카오 소셜 로그인 처리
  const handleKakaoLogin = async () => {
    try {
      const response = await SocialAxiosInstance.get("v1/auth/oauth2/kakao");
      if (response.data && response.data.redirectUrl) {
        window.location.href = response.data.redirectUrl; // 소셜 로그인 URL로 리디렉션
      } else {
        throw new Error("유효하지 않은 리디렉션 URL");
      }
    } catch (error) {
      console.error("카카오 로그인 실패:", error.response?.data || error.message);
      alert("카카오 로그인에 실패했습니다. 다시 시도해주세요.");
    }
  };

  return (
    <div id="sign-in-wrapper">
      <div className="sign-in-container">
        <div className="sign-in-box">
          <img src={logoImage} alt="AICFN Logo" className="sign-in-logo" />
          <h2 className="sign-in-title">로그인</h2>
          {errorMessage && <p className="error-message">{errorMessage}</p>}
          <form onSubmit={handleSubmit} className="sign-in-content-box">
            <div className="sign-in-content-input-box">
              <label htmlFor="id" className="sign-in-label">
                아이디
              </label>
              <input
                type="text"
                id="id"
                placeholder="아이디를 입력하세요."
                value={id}
                onChange={(e) => setId(e.target.value)}
                className="sign-in-input"
              />
            </div>
            <div className="sign-in-content-input-box">
              <label htmlFor="password" className="sign-in-label">
                비밀번호
              </label>
              <input
                type="password"
                id="password"
                placeholder="비밀번호를 입력하세요."
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="sign-in-input"
              />
            </div>
            <div className="sign-in-content-button-box">
              <button type="submit" className="sign-in-button">
                로그인
              </button>
            </div>
          </form>

          <div className="sign-in-content-divider"></div>

          {/* 카카오 간편 로그인 */}
          <div className="sign-in-content-sns-sign-up-box">
            <p className="sign-in-content-sns-sign-up-title">
              카카오 계정으로 간편 로그인
            </p>
            <div
              className="sign-in-content-sns-sign-up-button-box"
              onClick={handleKakaoLogin}
            >
              <img src={kakaoIcon} alt="Kakao Login" className="sign-in-social-icon" />
            </div>
          </div>

          <div className="sign-in-help-links">
            <Link to="/FindId" className="sign-in-link">
              아이디 찾기
            </Link>
            {" | "}
            <Link to="/FindPassword" className="sign-in-link">
              비밀번호 찾기
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;