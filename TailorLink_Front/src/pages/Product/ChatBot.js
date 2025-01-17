import React, { useState, useEffect, useRef } from "react";
import recommendAxiosInstance from "../../API/RecommendAxionInstance";
import ReactMarkdown from "react-markdown"; // 마크다운 처리
import "./ChatBot.css";

const features = [
  { id: 1, title: "차량 추천" },
  { id: 2, title: "보험 안내" },
  { id: 3, title: "차량 가이드" },
];

const ChatBot = () => {
  const [activeFeature, setActiveFeature] = useState(1);
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState("");
  const [isResponding, setIsResponding] = useState(false);
  const [sessionId, setSessionId] = useState(""); // 초기값 빈 문자열
  const [carImage, setCarImage] = useState("");
  const [suggestQuestions, setSuggestQuestions] = useState([]);
  const [showSuggestions, setShowSuggestions] = useState(true);
  const chatWindowRef = useRef(null);

  // 차량 추천 API 요청 함수
  const fetchCarRecommendation = async (userMessage) => {
    try {
      const response = await recommendAxiosInstance.post("/api/cars/car_recommend_chat", {
        session_id: sessionId || "",
        user_input: userMessage,
      });
      setSessionId(response.data.session_id);
      setCarImage(response.data.page_info?.car_image || "");
      setSuggestQuestions(response.data.suggest_question || []);
      return response.data.response;
    } catch (error) {
      console.error("차량 추천 오류:", error);
      return "추천 정보를 불러오는 데 실패했습니다. 다시 시도해주세요.";
    }
  };

  // 차량 가이드 API 요청 함수
  const fetchCarManual = async (userMessage) => {
    try {
      const userId = localStorage.getItem("userId") || "string"; // 사용자 ID
      const carId = 1; // 차량 ID (필요시 동적으로 가져오기)

      const response = await recommendAxiosInstance.post("/api/manuals/manual", {
        session_id: sessionId || "",
        user_input: userMessage,
        user_id: userId,
        car_id: carId,
      });
      setSessionId(response.data.session_id);
      return response.data.response;
    } catch (error) {
      console.error("차량 가이드 오류:", error);
      return "차량 가이드 정보를 불러오는 데 실패했습니다. 다시 시도해주세요.";
    }
  };

  // 메시지 전송 및 응답 처리
  const handleSendMessage = async (messageToSend = null) => {
    const userMessage = messageToSend || inputValue.trim();
    if (userMessage === "" || isResponding) return;

    setMessages((prev) => [...prev, { user: true, text: userMessage }]);
    setInputValue("");
    setIsResponding(true);
    setMessages((prev) => [...prev, { user: false, text: "메시지 생성중..." }]);

    let botResponse = "기능에 대한 정보를 불러오고 있습니다...";
    if (activeFeature === 1) {
      botResponse = await fetchCarRecommendation(userMessage);
    } else if (activeFeature === 3) {
      botResponse = await fetchCarManual(userMessage);
    } else {
      botResponse = "이 기능은 현재 준비 중입니다. 조금만 기다려주세요!";
    }

    setMessages((prev) => [...prev.slice(0, -1), { user: false, text: botResponse }]);
    setIsResponding(false);
  };

  // 서제스트 퀘스쳔 버튼 클릭 처리
  const handleSuggestQuestionClick = (question) => {
    handleSendMessage(question);
  };

  // 서제스트 퀘스쳔 닫기
  const handleCloseSuggestions = () => {
    setShowSuggestions(false);
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
              className={`feature-item ${activeFeature === feature.id ? "active" : ""}`}
              onClick={() => {
                setActiveFeature(feature.id);
                setMessages([]);
                setCarImage("");
                setSuggestQuestions([]);
                setShowSuggestions(true);
              }}
            >
              {feature.title}
            </li>
          ))}
        </ul>
      </div>

      <div className="chatbot-content-container">
        <div className="chatbot-main">
          <h2 className="chatbot-header">{features.find((f) => f.id === activeFeature).title}</h2>

          <div className="chat-window" ref={chatWindowRef}>
            {messages.map((msg, index) => (
              <div key={index} className={`chat-message ${msg.user ? "user-message" : "bot-message"}`}>
                {/* 차량 추천 및 가이드에 마크다운 적용 */}
                {(activeFeature === 1 || activeFeature === 3) && !msg.user ? (
                  <ReactMarkdown>{msg.text}</ReactMarkdown>
                ) : (
                  msg.text
                )}
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
            <button onClick={() => handleSendMessage()} disabled={isResponding}>
              보내기
            </button>
          </div>
        </div>

        <div className="chatbot-image-area">
          {activeFeature === 1 && carImage && <img src={carImage} alt="Car" className="car-image" />}
          {activeFeature === 1 && suggestQuestions.length > 0 && showSuggestions && (
            <div className="suggest-questions">
              {suggestQuestions.map((question, index) => (
                <button
                  key={index}
                  className="suggest-question-button"
                  onClick={() => handleSuggestQuestionClick(question)}
                >
                  {question}
                </button>
              ))}
              <button className="close-suggestions" onClick={handleCloseSuggestions}>
                ✖ 닫기
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ChatBot;