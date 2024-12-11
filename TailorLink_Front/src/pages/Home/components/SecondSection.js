import React, { useEffect, useRef, useState } from "react";
import "./Section.css"; // `Section.css` 파일이 같은 폴더 내에 있는 경우

const SecondSection = () => {
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
      <h2 style={styles.title}>AI</h2>
      <p style={styles.description}>
       이제는 <span style={styles.Highlight}>변화</span>할 때 입니다.
      </p>
      <ul style={styles.list}>
        <li>
        미래를 여는 기술, 지금 당신의 비즈니스에 도입하세요 
        </li>
        <li>
        AI를 적극 활용하지 않는 기업은 변화의 흐름에서 도태될 수 있습니다.
        </li>
        <li>
        AI의 힘을 경험하며 더 큰 성장을 경험 하세요.
          적절한 응답 생성.
        </li>
      </ul>
    </div>
  );
};

const styles = {
  section: {
    display: "flex", // Flexbox 사용
    flexDirection: "column", // 세로 정렬
    justifyContent: "center", // 수직 중앙 정렬
    alignItems: "center", // 수평 중앙 정렬
    height: "100vh", // 화면 전체 높이
    textAlign: "center", // 텍스트 중앙 정렬
    backgroundColor: "#042C38", // 배경색
    padding: "20px", // 내용 여백 추가
    boxSizing: "border-box",
  },
  
  title: {
    fontSize: "2rem",
    fontWeight: "bold",
    marginBottom: "20px",
    color: "#FF6161",
  },
  description: {
    fontSize: "1.2rem",
    color: "#555",
    maxWidth: "800px",
    lineHeight: "1.5",
    marginBottom: "30px",
  },
  Highlight: {
    color: "#FF6161",
    fontWeight: "bold",
    fontSize: "1.4rem", // 크기를 키움
    textShadow: "1px 1px 2px rgba(0, 0, 0, 0.2)", // 텍스트 그림자 추가 (선택)
  },
  list: {
    textAlign: "left", // 리스트는 왼쪽 정렬
    maxWidth: "800px",
    lineHeight: "1.8",
    color: "#555",
  },
};

export default SecondSection;