// Sidebar.js
import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import './Sidebar.css';

const Sidebar = ({ onWriteClick }) => {
  const location = useLocation();
  const isBoardActive = location.pathname.startsWith("/service/board");
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
