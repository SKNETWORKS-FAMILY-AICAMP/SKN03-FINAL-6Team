// Faq.js
import React from 'react';
import Sidebar from './Sidebar';
import './FAQ.css';

const Faq = () => {
  return (
    <div className="board-container">
      <Sidebar /> {/* 글쓰기 버튼 없음 */}
      <div className="board-main">
        <h2 className="board-title">FAQ</h2>
        <div className="faq-intro">
          <p>자주 묻는 질문을 모아놓은 곳입니다.</p>
          <p>여기서 원하는 답변을 찾을 수 없으면 1:1 문의하기를 이용해주세요.</p>
        </div>
        <div className="faq-list">
          <div className="faq-item">
            <h4>Q: 회원가입은 어떻게 하나요?</h4>
            <p>A: 우측 상단 회원가입 버튼을 클릭하여 진행할 수 있습니다.</p>
          </div>
          <div className="faq-item">
            <h4>Q: 비밀번호를 잊어버렸어요.</h4>
            <p>A: 로그인 페이지에서 '비밀번호 찾기'를 통해 재설정할 수 있습니다.</p>
          </div>
          <div className="faq-item">
            <h4>Q: 게시판에 글쓰기는 어떻게 하나요?</h4>
            <p>A: 게시판 페이지 왼쪽 상단의 '글쓰기' 버튼을 통해 작성 가능합니다.</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Faq;
