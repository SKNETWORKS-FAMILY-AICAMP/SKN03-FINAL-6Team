import React from "react";

const ContactUs = () => {
  return (
    <div style={styles.container}>
      <h1 style={styles.title}>주요 기능</h1>
      <p style={styles.description}>
        TailorLink의 주요 기능에 대해 알아보세요. 사용자 맞춤형 경험을 제공합니다.
      </p>
      <ul style={styles.featureList}>
        <li style={styles.featureItem}>사용자 맞춤형 프로필 설정</li>
        <li style={styles.featureItem}>고급 검색 및 필터 기능</li>
        <li style={styles.featureItem}>실시간 알림 및 공지</li>
      </ul>
    </div>
  );
};

const styles = {
  container: {
    padding: "40px",
    textAlign: "center",
    backgroundColor: "#f9f9f9",
    minHeight: "80vh",
  },
  title: {
    fontSize: "2rem",
    fontWeight: "bold",
    color: "#333",
    marginBottom: "20px",
  },
  description: {
    fontSize: "1rem",
    color: "#666",
    marginBottom: "30px",
  },
  featureList: {
    listStyleType: "none",
    padding: 0,
    margin: "0 auto",
    maxWidth: "600px",
    textAlign: "left",
  },
  featureItem: {
    backgroundColor: "#e6f0ff",
    padding: "10px 15px",
    borderRadius: "5px",
    marginBottom: "10px",
    fontSize: "1rem",
    color: "#333",
  },
};

export default ContactUs;