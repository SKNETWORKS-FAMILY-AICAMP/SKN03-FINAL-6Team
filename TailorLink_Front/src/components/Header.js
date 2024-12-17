import React from "react";
import { Link, useLocation } from "react-router-dom";
import "./Header.css";
import logoImage from "../assets/images/MainLogo.png";

const TopNav = () => {
  const location = useLocation();
  const isActive = (path) => location.pathname === path;

  return (
    <div className="header">
      <div className="header-container">
        {/* 로고 */}
        <Link to="/" className="logo">
          <img src={logoImage} alt="TailorLink Logo" />
        </Link>

        {/* 네비게이션 링크 */}
        <nav className="nav">
          <ul className="nav-list">
            <li className="nav-item">
              <Link
                to="/"
                className={`nav-link ${isActive("/") ? "active" : ""}`}
              >
                홈
              </Link>
            </li>
            <li className="nav-item">
              {/* 라우팅 경로를 `/Product/ChatBot`으로 변경 */}
              <Link
                to="/Product/ChatBot"
                className={`nav-link ${
                  isActive("/Product/ChatBot") ? "active" : ""
                }`}
              >
                기능
              </Link>
            </li>
            <li className="nav-item">
              <Link
                to="/service/board"
                className={`nav-link ${
                  isActive("/service/board") ? "active" : ""
                }`}
              >
                고객센터
              </Link>
            </li>
          </ul>
        </nav>

        {/* 로그인/회원가입 */}
        <div className="auth-links">
          <Link
            to="/login"
            className={`auth-link ${isActive("/login") ? "active" : ""}`}
          >
            로그인
          </Link>
          <Link
            to="/register"
            className={`auth-link ${isActive("/register") ? "active" : ""}`}
          >
            회원가입
          </Link>
        </div>
      </div>
    </div>
  );
};

export default TopNav;
