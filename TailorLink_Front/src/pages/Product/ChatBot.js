import React, { useState, useEffect, useRef } from "react";
import SwaggerUI from "swagger-ui-react";
import "swagger-ui-react/swagger-ui.css";
import "./ChatBot.css";

const features = [
  { id: 0, title: "New Chat" },
  { id: 1, title: "차량 추천" }, // Swagger UI가 여기에만 활성화됨
  { id: 2, title: "보험 안내" },
  { id: 3, title: "차량 가이드" },
];

const ChatBot = () => {
  const [activeFeature, setActiveFeature] = useState(0);
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState("");
  const [isResponding, setIsResponding] = useState(false);

  const chatWindowRef = useRef(null);

  // 메시지 입력 및 응답 처리
  const handleSendMessage = () => {
    if (inputValue.trim() === "" || isResponding) return;

    const userMessage = inputValue.trim();
    setMessages((prev) => [...prev, { user: true, text: userMessage }]);
    setIsResponding(true);
    setTimeout(() => setInputValue(""), 0);

    setTimeout(() => {
      setMessages((prev) => [
        ...prev,
        { user: false, text: "기능에 대한 정보를 불러오고 있습니다..." },
      ]);
      setIsResponding(false);
    }, 500);
  };

  // 스크롤 하단 이동
  useEffect(() => {
    if (chatWindowRef.current) {
      chatWindowRef.current.scrollTop = chatWindowRef.current.scrollHeight;
    }
  }, [messages]);

  return (
    <div className="chatbot-container">
      <div className="chatbot-sidebar">
        <h3>기능 선택</h3>
        <ul className="feature-list">
          {features.map((feature) => (
            <li
              key={feature.id}
              className={`feature-item ${
                activeFeature === feature.id ? "active" : ""
              }`}
              onClick={() => {
                setActiveFeature(feature.id);
                setMessages([]); // 새로운 기능 선택 시 메시지 초기화
              }}
            >
              {feature.title}
            </li>
          ))}
        </ul>
      </div>

      <div className="chatbot-content-container">
        <div className="chatbot-main">
          <h2 className="chatbot-header">
            {features.find((f) => f.id === activeFeature).title}
          </h2>

          {/* 차량 추천(id=1)에서만 Swagger UI 활성화 */}
          {activeFeature === 1 ? (
            <SwaggerUI url="http://dkwcdr.iptime.org:8000/docs" />
          ) : (
            <>
              <div className="chat-window" ref={chatWindowRef}>
                {messages.map((msg, index) => (
                  <div
                    key={index}
                    className={`chat-message ${
                      msg.user ? "user-message" : "bot-message"
                    }`}
                  >
                    {msg.text}
                  </div>
                ))}
              </div>
              <div className="chat-input">
                <input
                  type="text"
                  placeholder="메시지를 입력하세요..."
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === "Enter") handleSendMessage();
                  }}
                />
                <button onClick={handleSendMessage} disabled={isResponding}>
                  보내기
                </button>
              </div>
            </>
          )}
        </div>

        <div className="chatbot-image-area">
          <p>이미지 또는 추가 콘텐츠 영역</p>
        </div>
      </div>
    </div>
  );
};

export default ChatBot;
