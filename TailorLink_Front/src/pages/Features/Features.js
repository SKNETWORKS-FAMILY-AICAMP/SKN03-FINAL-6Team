import React, { useState } from "react";
import "./Features.css";

// 이미지 가져오기
import carRecommendation from "../../assets/images/P.png";
import carManual from "../../assets/images/R.png";
import insurance from "../../assets/images/Pi.png";
import estimate from "../../assets/images/G.png";

const Features = () => {
  const [activeChatbot, setActiveChatbot] = useState(null);

  const features = [
    { id: 1, title: "차량 추천 AI", image: carRecommendation, chatbot: "차량추천 Bot" },
    { id: 2, title: "차량 매뉴얼 AI", image: carManual, chatbot: "차량 메뉴얼 Bot" },
    { id: 3, title: "보험 상담 AI", image: insurance, chatbot: "보험상담 Bot" },
    { id: 4, title: "견적 내기 AI", image: estimate, chatbot: "간단 견적내기" },
  ];

  const handleCardClick = (id) => {
    if (activeChatbot === id) {
      setActiveChatbot(null);
    } else {
      setActiveChatbot(id);
    }
  };

  return (
    <div className="features-page">
      <div className="features-container">
        {features.map((feature) => (
          <div
            key={feature.id}
            className="feature-card"
            onClick={() => handleCardClick(feature.id)}
          >
            <img src={feature.image} alt={feature.title} className="feature-image" />
            <div className="feature-title">{feature.title}</div>
          </div>
        ))}
      </div>

      {activeChatbot && (
        <div className="chatbot-container">
          <div className="chatbot-header">
            {features.find((feature) => feature.id === activeChatbot).chatbot}
          </div>
          <div className="chatbot-messages">
            {/* 더미 메시지 */}
            <div className="message bot">안녕하세요! 무엇을 도와드릴까요?</div>
            <div className="message user">안녕</div>
          </div>
          <div className="chatbot-input-container">
            <input
              type="text"
              className="chatbot-input"
              placeholder="메시지를 입력하세요..."
            />
            <button className="chatbot-send-button">보내기</button>
          </div>
        </div>
      )}
    </div>
  );
};

export default Features;