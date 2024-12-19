// Sidebar.js
import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import './Sidebar.css';

const Sidebar = ({ onWriteClick }) => {
  const location = useLocation();

  // 활성화 판단 함수
  // 전체게시판: /service/board 경로일 때 활성화
  // 1:1문의하기: /service/qna 경로일 때 활성화
  // FAQ: /service/faq 경로일 때 활성화
  const isBoardActive = location.pathname.startsWith("/service/board");
  const isQnaActive = location.pathname === "/service/qna";
  const isFaqActive = location.pathname === "/service/faq";

  return (
    <aside className="board-sidebar">
      {onWriteClick && (
        <button className="write-btn" onClick={onWriteClick}>글쓰기</button>
      )}
      <ul className="menu-list">
        <li>
          <Link
            to="/service/board"
            className={`sidebar-link ${isBoardActive ? "active" : ""}`}
          >
            전체 게시판
          </Link>
        </li>
        <li>
          <Link
            to="/service/qna"
            className={`sidebar-link ${isQnaActive ? "active" : ""}`}
          >
            1:1 문의하기
          </Link>
        </li>
        <li>
          <Link
            to="/service/faq"
            className={`sidebar-link ${isFaqActive ? "active" : ""}`}
          >
            FAQ
          </Link>
        </li>
      </ul>
    </aside>
  );
};

export default Sidebar;
