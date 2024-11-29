import React, { useEffect, useRef, useState } from "react";
import mainImage from "../../../assets/images/Main.png";
import mainImage2 from "../../../assets/images/Main2.png"; // 이미지 경로 import
import "./Section.css"; // 추가 스타일 적용

const FirstSection = () => {
  const sectionRef = useRef(null);
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            setIsVisible(true);
          }
        });
      },
      { threshold: 0.5 }
    );

    if (sectionRef.current) {
      observer.observe(sectionRef.current);
    }

    return () => {
      if (sectionRef.current) observer.unobserve(sectionRef.current);
    };
  }, []);

  return (
    <div
      ref={sectionRef}
      className={`section ${isVisible ? "visible" : ""}`}
      style={styles.section}
    >
      <div className="solutions-container" style={styles.solutionsContainer}>
        {/* Solution 1: 이미지 왼쪽, 텍스트 오른쪽 */}
        <div className="solution-card1" style={styles.card}>
          <img src={mainImage} alt="AI Solutions" style={styles.cardImage} />
          <div style={styles.cardContent}>
            <h2 style={styles.cardTitle}>AI Solutions</h2>
            <p style={styles.cardSubtitle}>“원스톱 솔루션 제공”</p>
            <p style={styles.cardSubtitle}>AI Chatbot으로 혁신을 만나다</p>
            <p style={styles.cardText}>
              Tailor Link는 AI ChatBot을 통한 다양한 서비스를 통합적으로
              제공하여 편리함과 전문성을 동시에 경험할 수 있습니다.
            </p>
          </div>
        </div>

        {/* Solution 2: 텍스트 왼쪽, 이미지 오른쪽 */}
        <div className="solution-card2" style={styles.cardReverse}>
          <div style={styles.cardContent}>
            <h2 style={styles.cardTitle}>Automation System</h2>
            <p style={styles.cardSubtitle}>“AI를 통한 업무 자동화”</p>
            <p style={styles.cardText}>
              AI 솔루션으로 반복적이고 복잡한 작업을 자동화하여 생산성을 극대화하고
              중요한 업무에 집중할 수 있는 환경을 만듭니다.
            </p>
          </div>
          <img src={mainImage2} alt="Automation System" style={styles.cardImage} />
        </div>
      </div>
    </div>
  );
};

const styles = {
  section: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    padding: "50px 20px",
    background: "#FFFFFF",
  },
  solutionsContainer: {
    display: "flex",
    flexDirection: "column",
    gap: "20px",
    maxWidth: "1000px",
    width: "100%",
  },
  card: {
    display: "flex",
    flexDirection: "row",
    alignItems: "center",
    backgroundColor: "#ffffff",
    boxShadow: "0 4px 8px rgba(0, 0, 0, 0.1)",
    borderRadius: "10px",
    overflow: "hidden",
  },
  cardReverse: {
    display: "flex",
    flexDirection: "reverse", // 반대로 정렬
    alignItems: "center",
    backgroundColor: "#ffffff",
    boxShadow: "0 4px 8px rgba(0, 0, 0, 0.1)",
    borderRadius: "10px",
    overflow: "hidden",
  },
  cardImage: {
    flex: "1 1 0",
    objectFit: "cover",
    height: "250px",
    width: "100%",
  },
  cardContent: {
    flex: "1",
    padding: "20px",
    textAlign: "left",
  },
  cardTitle: {
    fontSize: "1.8rem",
    fontWeight: "bold",
    color: "#333",
    marginBottom: "10px",
  },
  cardSubtitle: {
    fontSize: "1.1rem",
    color: "#555",
    marginBottom: "10px",
  },
  cardText: {
    fontSize: "1rem",
    color: "#555",
  },
};

export default FirstSection;