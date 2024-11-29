import React, { useState } from "react";
import { Link, useLocation } from "react-router-dom";
import "./Header.css";
import logoImage from "../assets/images/TailorLink.png";

const TopNav = () => {
  const [isDropdownVisible, setIsDropdownVisible] = useState(false);
  const location = useLocation();

  const handleMouseEnter = () => {
    setIsDropdownVisible(true);
  };

  const handleMouseLeave = () => {
    setIsDropdownVisible(false);
  };

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
              <Link
                to="/guide"
                className={`nav-link ${isActive("/guide") ? "active" : ""}`}
              >
                가이드
              </Link>
            </li>
            <li className="nav-item">
              <Link
                to="/features"
                className={`nav-link ${isActive("/features") ? "active" : ""}`}
              >
                기능
              </Link>
            </li>

            {/* 고객센터 드롭다운 */}
            <li
              className="nav-item"
              onMouseEnter={handleMouseEnter}
              onMouseLeave={handleMouseLeave}
            >
              <span className="nav-link">고객센터</span>
              {isDropdownVisible && (
                <div className="dropdown">
                  <div className="left-section">
                    <ul>
                      <li>
                        <Link
                          to="/service/contactus"
                          className={`dropdown-link ${
                            isActive("/service/contactus") ? "active" : ""
                          }`}
                        >
                          문의하기
                        </Link>
                      </li>
                      <li>
                        <Link
                          to="/service/board"
                          className={`dropdown-link ${
                            isActive("/service/board") ? "active" : ""
                          }`}
                        >
                          게시판
                        </Link>
                      </li>
                    </ul>
                  </div>
                </div>
              )}
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