import React from "react";
import "./ThirdSection.css";

const ThirdSection = () => {
  const features = [
    { id: 1, title: "준비중", status: "inactive" },
    { id: 2, title: "AI 상품 추천", status: "active" },
    { id: 3, title: "AI 상품 견적", status: "active" },
    { id: 4, title: "AI 사내 문서 분석", status: "active" },
    { id: 5, title: "AI 상담 챗봇", status: "active" },
    { id: 6, title: "준비중", status: "inactive" },
  ];

  return (
    <div className="third-section">
      <h2 className="third-section-title">TailorLink의 여러 기능들</h2>
      <div className="features-container">
        {features.map((feature) => (
          <div
            key={feature.id}
            className={`feature-card ${
              feature.status === "inactive" ? "inactive" : "active"
            }`}
          >
            <div className="feature-card-content">
              <p>{feature.title}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ThirdSection;