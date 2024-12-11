import React, { useState } from "react";
import logoImage from "../../assets/images/TailorLink.png"; // TailorLink 로고 이미지 경로
import kakaoIcon from "../../assets/images/kakao.png"; // 카카오 아이콘 이미지 경로
import naverIcon from "../../assets/images/naver.png"; // 네이버 아이콘 이미지 경로
import googleIcon from "../../assets/images/google.png"; // 구글 아이콘 이미지 경로

const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("로그인 정보:", { email, password });
  };

  return (
    <div style={styles.container}>
      <img src={logoImage} alt="TailorLink Logo" style={styles.logo} />
      <div style={styles.loginBox}>
        <h2 style={styles.title}>로그인</h2>
        <form onSubmit={handleSubmit} style={styles.form}>
          <div style={styles.inputGroup}>
            <label htmlFor="email" style={styles.label}>이메일</label>
            <input
              type="email"
              id="email"
              placeholder="이메일을 입력하세요."
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              style={styles.input}
            />
          </div>
          <div style={styles.inputGroup}>
            <label htmlFor="password" style={styles.label}>비밀번호</label>
            <input
              type="password"
              id="password"
              placeholder="비밀번호를 입력하세요."
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              style={styles.input}
            />
          </div>
          <button type="submit" style={styles.button}>로그인</button>
        </form>
        <div style={styles.helpLinks}>
          <a href="/find-id" style={styles.link}>아이디 찾기</a> |{" "}
          <a href="/reset-password" style={styles.link}>비밀번호 찾기</a>
        </div>
        <p style={styles.socialLoginText}>소셜 계정으로 간편 로그인</p>
        <div style={styles.socialIcons}>
          <img src={kakaoIcon} alt="Kakao Login" style={styles.socialIcon} />
          <img src={naverIcon} alt="Naver Login" style={styles.socialIcon} />
          <img src={googleIcon} alt="Google Login" style={styles.socialIcon} />
        </div>
      </div>
    </div>
  );
};

const styles = {
  container: {
    display: "flex",
    flexDirection: "column",
    justifyContent: "flex-start",
    alignItems: "center",
    minHeight: "100vh",
    backgroundColor: "#E6F0FF",
    padding: "20px",
  },
  logo: {
    width: "150px",
    marginBottom: "30px",
  },
  loginBox: {
    backgroundColor: "#C9E6FF",
    borderRadius: "10px",
    padding: "30px",
    boxShadow: "0px 4px 10px rgba(0, 0, 0, 0.1)",
    width: "100%",
    maxWidth: "300px",
    textAlign: "center",
  },
  title: {
    fontSize: "1.5rem",
    fontWeight: "bold",
    marginBottom: "20px",
  },
  form: {
    display: "flex",
    flexDirection: "column",
    gap: "15px",
  },
  inputGroup: {
    textAlign: "left",
  },
  label: {
    fontSize: "0.9rem",
    marginBottom: "5px",
    color: "#333",
  },
  input: {
    width: "100%",
    padding: "10px",
    fontSize: "1rem",
    borderRadius: "5px",
    border: "1px solid #ccc",
    boxSizing: "border-box",
  },
  button: {
    backgroundColor: "#4A90E2",
    color: "#FFF",
    border: "none",
    borderRadius: "5px",
    padding: "10px",
    fontSize: "1rem",
    cursor: "pointer",
    transition: "background-color 0.3s",
  },
  buttonHover: {
    backgroundColor: "#357ABD",
  },
  helpLinks: {
    marginTop: "15px",
    fontSize: "0.8rem",
  },
  link: {
    color: "#4A90E2",
    textDecoration: "none",
  },
  socialLoginText: {
    marginTop: "20px",
    fontSize: "0.9rem",
    color: "#333",
  },
  socialIcons: {
    display: "flex",
    justifyContent: "center",
    gap: "35px",
    marginTop: "10px",
  },
  socialIcon: {
    width: "40px",
    height: "40px",
    cursor: "pointer",
  },
};

export default Login;