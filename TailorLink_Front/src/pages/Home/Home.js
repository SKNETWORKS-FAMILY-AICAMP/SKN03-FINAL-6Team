import React, { useState, useEffect } from "react";
import "./Home.css";
import aicfnImage from "../../assets/images/AICFN.png";
import carImage from "../../assets/images/Car1.png";

const Home = () => {
  const [currentSlide, setCurrentSlide] = useState(0);
  const [typedText, setTypedText] = useState("");
  const [typingIndex, setTypingIndex] = useState(0);
  const [hasTypedOnce, setHasTypedOnce] = useState(false);
  const [isTyping, setIsTyping] = useState(true);
  const [isAutoSliding, setIsAutoSliding] = useState(true);

  const slides = [
    {
      image: aicfnImage,
      title: "AICFN",
      description:
        "운전자를 위한 AI 기반 차량 관리 서비스로, 차량 추천부터 유지 관리까지 한 번에 해결하세요.",
    },
    {
      image: carImage,
      title: "차량 추천",
      description:
        "사용자의 필요와 예산에 맞는 최적의 차량을 추천하며, 맞춤형 정보를 제공합니다.",
    },
    {
      title: "기능 소개",
      description: "아래에서 원하는 기능을 선택하고 경험해보세요!",
      isMultiSection: true,
      sections: [
        {
          title: "차량 추천",
          description: "필요와 예산에 맞는 차량 추천 서비스.",
          buttonText: "차량 추천 보러 가기",
          link: "/Product/ChatBot?feature=recommend",
        },
        {
          title: "보험 안내",
          description: "보험 상품 비교 및 상담 서비스.",
          buttonText: "보험 안내 보러 가기",
          link: "/Product/ChatBot?feature=insurance",
        },
        {
          title: "차량 가이드",
          description: "차량 사용법 및 유지 관리 가이드.",
          buttonText: "차량 가이드 보러 가기",
          link: "/Product/ChatBot?feature=guide",
        },
      ],
    },
  ];

  useEffect(() => {
    if (isTyping || !isAutoSliding) return;

    const timer = setTimeout(() => {
      setCurrentSlide((prev) => {
        const nextSlide = (prev + 1) % slides.length;
        if (nextSlide === 0) {
          setIsAutoSliding(false);
          setHasTypedOnce(true);
        }
        return nextSlide;
      });
      setIsTyping(true);
    }, 1000);

    return () => clearTimeout(timer);
  }, [isTyping, isAutoSliding, currentSlide, slides.length]);

  useEffect(() => {
    setTypedText("");
    setTypingIndex(0);
    setIsTyping(true);
  }, [currentSlide]);

  useEffect(() => {
    const currentText = slides[currentSlide].description || "";

    if (!hasTypedOnce && typingIndex < currentText.length) {
      const timeout = setTimeout(() => {
        setTypedText((prev) => prev + currentText[typingIndex]);
        setTypingIndex((prev) => prev + 1);
      }, 50);

      return () => clearTimeout(timeout);
    } else if (typingIndex === currentText.length) {
      setIsTyping(false);
    } else if (hasTypedOnce) {
      setTypedText(currentText);
      setIsTyping(false);
    }
  }, [typingIndex, currentSlide, slides, hasTypedOnce]);

  const handleSlideChange = (index) => {
    setCurrentSlide(index);
    setHasTypedOnce(true);
    setIsAutoSliding(false);
    setIsTyping(false);
  };

  return (
    <div className="home-container">
      <div className="slides-wrapper">
        {slides.map((slide, index) => (
          <div
            key={index}
            className={`slide ${index === currentSlide ? "active" : ""}`}
          >
            {slide.image && (
              <img src={slide.image} alt={slide.title} className="image" />
            )}
            <div className="content">
              <h2>{slide.title}</h2>
              <p className="typing-effect">{typedText}</p>
              {slide.isMultiSection ? (
                <div className="sections-container">
                  {slide.sections.map((section, secIndex) => (
                    <div key={secIndex} className="section">
                      <h3>{section.title}</h3>
                      <p>{section.description}</p>
                      <button
                        className="navigate-button"
                        onClick={() => (window.location.href = section.link)}
                      >
                        {section.buttonText}
                      </button>
                    </div>
                  ))}
                </div>
              ) : (
                slide.button && (
                  <button
                    className="navigate-button"
                    onClick={() => {
                      window.location.href = "/Product/ChatBot";
                    }}
                  >
                    기능 섹션으로 이동
                  </button>
                )
              )}
            </div>
          </div>
        ))}
      </div>

      <div className="pagination-buttons">
        {slides.map((_, index) => (
          <div
            key={index}
            className={`pagination-button ${
              index === currentSlide ? "active" : ""
            }`}
            onClick={() => handleSlideChange(index)}
          ></div>
        ))}
      </div>
    </div>
  );
};

export default Home;