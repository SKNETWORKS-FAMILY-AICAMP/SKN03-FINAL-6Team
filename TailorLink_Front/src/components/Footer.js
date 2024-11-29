import React from "react";

const Footer = () => {
  return (
    <footer style={styles.footer}>
      <div style={styles.Text}>
      <div style={styles.info}>
        <p>
          주식회사 TailorLink | 대표 최연규 | 주소 서울특별시 금천구 대륭테크노타운 17차 18층
          PlayData
        </p>
        <p>
          고객센터 010-2972-5**4 | Email bkwcdr@google.com | 운영시간 평일 09:00 ~ 18:00
        </p>
        <p>사업자등록번호 000-00-00000</p>
      </div>
      <div style={styles.links}>
        <a href="https://www.instagram.com/yg._.yu/" style={styles.link}>이용약관</a> |{" "}
        <a href="https://www.instagram.com/_o1.31/" style={styles.link}>개인정보처리방침</a>
      </div>
      <p style={styles.copyright}>
        Copyright ©2024 TailorLink. All rights reserved.
      </p>
      </div>
    </footer>
  );
};

const styles = {
  footer: {
    backgroundColor: "#042c38", // 푸터 배경색
    textAlign: "left",
    padding: "10px",
    fontSize: "0.9rem",
    color: "#666",
    marginTop: "auto", // 푸터를 하단에 고정
  },
  Text: {
    marginLeft: "20px",
  },
  info: {
    marginBottom: "8px",
    lineHeight: "1.6",
  },
  links: {
    marginBottom: "10px",
  },
  link: {
    color: "#007BFF", // 링크 색상
    textDecoration: "none",
    margin: "0 5px",
  },
  copyright: {
    fontSize: "0.7rem",
    color: "#999",
  },
};

export default Footer;