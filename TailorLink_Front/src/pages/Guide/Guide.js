import React from "react";
import "./Guide.css";

const Guide = () => {
  const guides = [
    { id: 1, text: "자주묻는 질문을 확인해보세요!!" },
    { id: 2, text: "테일러링크 사용법이 궁금하세요?" },
    { id: 3, text: "서비스 이용은 어떻게 하나요?" },
    { id: 4, text: "회원가입 방법은 어디에 있나요?" },
    { id: 5, text: "간단 견적내기 서비스는 어떻게 진행되나요?" },
    { id: 6, text: "AI 솔루션을 구매하고 싶어요!" },
  ];

  return (
    <div className="guide-container">
      <h1 className="guide-title">테일러링크를 사용해보세요.</h1>
      <div className="guide-description">
        <i className="info-icon">ℹ️</i>
        <p>
          <span className="highlight">질문</span>을 클릭하면{" "}
          <span className="highlight">챗봇</span>이 열립니다.
        </p>
      </div>
      <div className="card-grid">
        {guides.map((guide) => (
          <div key={guide.id} className="card">
            <div className="bubble">{guide.text}</div>
            <div className="card-icon">➔</div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Guide;