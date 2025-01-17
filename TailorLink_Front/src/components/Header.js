import React, { useContext, useEffect } from "react";
import { Link, useLocation } from "react-router-dom";
import "./Header.css";
import logoImage from "../assets/images/MainLogo.png";
import myPageIcon from "../assets/images/MyPage.png"; // 마이페이지 이미지
import logoutIcon from "../assets/images/Logout.png"; // 로그아웃 이미지
import { AuthContext } from "../API/AuthContext";


const TopNav = () => {
  const location = useLocation();
  const { isLoggedIn, setIsLoggedIn } = useContext(AuthContext);

  useEffect(() => {
    const token = localStorage.getItem("authToken");
    if (token) {
      setIsLoggedIn(true);
    }
  }, [setIsLoggedIn]);

  const handleLogout = () => {
    localStorage.removeItem("authToken");
    setIsLoggedIn(false);
    alert("로그아웃 되었습니다.");
  };

  const isActive = (path) => location.pathname === path;

  return (
    <header className="header">
      <div className="header-container">
        <Link to="/" className="logo">
          <img src={logoImage} alt="AICFN Logo" />
        </Link>
        <nav className="nav">
          <ul className="nav-list">
            <li className="nav-item">
              <Link to="/" className={`nav-link ${isActive("/") ? "active" : ""}`}>
                홈
              </Link>
            </li>
            <li className="nav-item">
              <Link
                to="/Product/ChatBot"
                className={`nav-link ${isActive("/Product/ChatBot") ? "active" : ""}`}
              >
                기능
              </Link>
            </li>
            <li className="nav-item">
              <Link
                to="/service/board"
                className={`nav-link ${isActive("/service/board") ? "active" : ""}`}
              >
                고객센터
              </Link>
            </li>
          </ul>
        </nav>
        <div className="auth-links">
          {isLoggedIn ? (
            <>
              <Link to="/mypage" className="auth-link">
                <img src={myPageIcon} alt="마이페이지" className="icon" />
              </Link>
              <button onClick={handleLogout} className="logout-button">
                <img src={logoutIcon} alt="로그아웃" className="icon" />
              </button>
            </>
          ) : (
            <>
              <Link to="/login" className={`auth-link ${isActive("/login") ? "active" : ""}`}>
                로그인
              </Link>
              <Link to="/register" className={`auth-link ${isActive("/register") ? "active" : ""}`}>
                회원가입
              </Link>
            </>
          )}
        </div>
      </div>
    </header>
  );
};

export default TopNav;