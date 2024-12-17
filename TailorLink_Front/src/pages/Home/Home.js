import React, { useState, useEffect } from "react";
import "./Home.css";
import FirstSection from "./components/FirstSection";
import ElevatorSection from "./components/ElevatorSection";
import TextSection from "./components/TextSection";

const Home = () => {
  const [stage, setStage] = useState(0);

  const handleScroll = () => {
    const scrollY = window.scrollY;
    const windowHeight = window.innerHeight;

    if (scrollY < windowHeight * 0.5) {
      setStage(0); // AICFN 이미지 표시
    } else if (scrollY >= windowHeight * 0.5 && scrollY < windowHeight * 1.5) {
      setStage(1); // 문 닫힘 애니메이션
    } else {
      setStage(2); // 텍스트 섹션 표시
    }
  };

  useEffect(() => {
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  return (
    <div className="home-container">
      <FirstSection stage={stage} />
      {stage >= 1 && <ElevatorSection stage={stage} />}
      {stage === 2 && <TextSection />}
    </div>
  );
};

export default Home;
