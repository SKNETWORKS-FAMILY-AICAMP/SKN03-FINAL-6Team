import React, { useState } from "react";
import logoImage from "../../assets/images/TailorLink.png";

const Register = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [name, setName] = useState("");
  const [phone, setPhone] = useState("");
  const [errorMessage, setErrorMessage] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (password !== confirmPassword) {
      setErrorMessage("비밀번호가 일치하지 않습니다.");
      return;
    }
    if (!/^(?=.*[a-zA-Z])(?=.*\d)(?=.*[!@#$%^&*()]).{8,}$/.test(password)) {
      setErrorMessage("비밀번호는 영문, 숫자, 특수문자를 포함하여 8자리 이상으로 구성해야 합니다.");
      return;
    }
    setErrorMessage("");
    console.log("회원가입 정보:", { email, password, name, phone });
  };

  return (
    <div style={styles.container}>
      <img src={logoImage} alt="TailorLink Logo" style={styles.logo} />
      <p style={styles.loginPrompt}>
        계정이 이미 있으신가요? <a href="/login" style={styles.loginLink}>로그인 하기</a>
      </p>
      <form onSubmit={handleSubmit} style={styles.form}>
        <div style={styles.inputRow}>
          <input
            type="email"
            placeholder="이메일을 입력하세요."
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            style={styles.input}
          />
          <button type="button" style={styles.checkButton}>중복확인</button>
        </div>
        <input
          type="password"
          placeholder="비밀번호를 입력하세요."
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          style={styles.input}
        />
        <input
          type="password"
          placeholder="비밀번호를 다시 입력하세요."
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
          style={styles.input}
        />
        {errorMessage && <p style={styles.errorMessage}>{errorMessage}</p>}
        <input
          type="text"
          placeholder="이름을 입력하세요."
          value={name}
          onChange={(e) => setName(e.target.value)}
          style={styles.input}
        />
        <input
          type="text"
          placeholder="휴대폰 번호를 입력하세요."
          value={phone}
          onChange={(e) => setPhone(e.target.value)}
          style={styles.input}
        />
        <button type="submit" style={styles.submitButton}>회원가입</button>
      </form>
    </div>
  );
};

const styles = {
  container: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    backgroundColor: "#E6F0FF",
    minHeight: "100vh",
    padding: "20px",
  },
  logo: {
    width: "150px",
    marginBottom: "10px",
  },
  loginPrompt: {
    fontSize: "0.9rem",
    marginBottom: "20px",
  },
  loginLink: {
    color: "#4A90E2",
    textDecoration: "none",
  },
  form: {
    display: "flex",
    flexDirection: "column",
    gap: "15px",
    width: "100%",
    maxWidth: "500px",
  },
  inputRow: {
    display: "flex",
    gap: "10px",
  },
  input: {
    width: "100%",
    padding: "10px",
    fontSize: "1rem",
    borderRadius: "5px",
    border: "1px solid #ccc",
    boxSizing: "border-box",
  },
  checkButton: {
    padding: "10px 15px",
    backgroundColor: "#4A90E2",
    color: "#FFF",
    border: "none",
    borderRadius: "5px",
    cursor: "pointer",
    whiteSpace: "nowrap",
  },
  errorMessage: {
    fontSize: "0.8rem",
    color: "red",
    marginTop: "-10px",
  },
  submitButton: {
    backgroundColor: "#4A90E2",
    color: "#FFF",
    border: "none",
    borderRadius: "5px",
    padding: "10px",
    fontSize: "1rem",
    cursor: "pointer",
    marginTop: "20px",
  },
};

export default Register;