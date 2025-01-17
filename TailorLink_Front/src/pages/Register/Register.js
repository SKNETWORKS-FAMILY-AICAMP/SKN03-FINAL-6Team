import React, { useState } from "react";
import { useNavigate } from "react-router-dom"; // 페이지 이동을 위한 useNavigate
import axiosInstance from "../../API/AxiosInstance";
import "./Register.css";

const Register = () => {
  const [id, setId] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [name, setName] = useState("");
  const [phone, setPhone] = useState("");
  const [verificationCode, setVerificationCode] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const [successMessage, setSuccessMessage] = useState("");
  const [passwordError, setPasswordError] = useState("");

  const navigate = useNavigate(); // 페이지 이동을 위한 useNavigate

  const handleIdCheck = async () => {
    try {
      const response = await axiosInstance.post(`/v1/auth/id-check`, { id: id });

      if (response.data.message === "Success") {
        setSuccessMessage("아이디 사용 가능합니다.");
        setErrorMessage("");
        window.alert("사용 가능한 아이디입니다.");
      }
      console.log("아이디 중복 확인 성공:", response.data);
    } catch (error) {
      const errorMsg =
        error.response?.data?.code === "DI" ? "아이디 중복 확인 실패 : 이미 사용 중인 아이디입니다." : ""
      setErrorMessage(errorMsg);
      console.error("아이디 중복 확인 실패:", error.response?.data || error.message);
      window.alert(errorMsg);
    }
  };

  const handleEmailVerification = async () => {
    try {
      const response = await axiosInstance.post(`/v1/auth/email-certification`, {
        id: id,
        email: email,
      });
      setSuccessMessage("이메일 인증번호가 전송되었습니다.");
      setErrorMessage("");
      window.alert("인증을 요청했습니다.");
    } catch (error) {
      const errorMsg =
        error.response?.data?.message || "이메일 인증 요청 실패: 다시 시도해주세요.";
      setErrorMessage(errorMsg);
    }
  };

  const handleVerificationCodeCheck = async () => {
    try {
      const response = await axiosInstance.post(
        `/v1/auth/check-certification`,
        { id: id, email: email, certificationNumber: verificationCode }
      );
      setSuccessMessage("이메일 인증이 완료되었습니다.");
      setErrorMessage("");
      window.alert("인증이 완료되었습니다.");
    } catch (error) {
      const errorMsg =
        error.response?.data?.message || "인증번호 확인 실패: 인증번호가 올바르지 않습니다.";
      setErrorMessage(errorMsg);
    }
  };

  const handleConfirmPasswordChange = (value) => {
    setConfirmPassword(value);
    if (password !== value) {
      setPasswordError("비밀번호가 일치하지 않습니다.");
    } else {
      setPasswordError("");
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (passwordError) {
      return;
    }

    if (!/^(?=.*[a-zA-Z])(?=.*[0-9])[a-zA-Z0-9]{8,13}$/.test(password)) {
      setErrorMessage(
        "비밀번호는 영문과 숫자를 포함하여 8~13자리로 구성해야 합니다."
      );
      return;
    }

    try {
      const response = await axiosInstance.post("/v1/auth/sign-up", {
        id: id,
        password: password,
        email: email,
        name: name,
        phoneNumber: phone,
        certificationNumber: verificationCode,
      });

      setSuccessMessage("회원가입에 성공했습니다!");
      setErrorMessage("");
      window.alert("회원가입에 성공했습니다!"); // 회원가입 성공 팝업
      navigate("/"); // 홈페이지로 이동
    } catch (error) {
      const errorMsg =
        error.response?.data?.message || "회원가입 실패: 요청을 확인해주세요.";
      setErrorMessage(errorMsg);
    }
  };

  return (
    <div className="register-wrapper">
      <div className="register-container">
        <h1 className="register-title">회원가입</h1>
        <p className="login-prompt">
          아이디가 이미 있으신가요?{" "}
          <span onClick={() => navigate("/login")} className="login-link">
            로그인하기
          </span>
        </p>
        {errorMessage && <p className="error-message">{errorMessage}</p>}
        {successMessage && <p className="success-message">{successMessage}</p>}

        <form onSubmit={handleSubmit} className="register-form">
          <div className="form-group">
            <label>아이디</label>
            <div className="input-row">
              <input
                type="text"
                placeholder="아이디를 입력하세요"
                value={id}
                onChange={(e) => setId(e.target.value)}
                className="input-field"
              />
              <button type="button" className="check-button" onClick={handleIdCheck}>
                중복 확인
              </button>
            </div>
          </div>

          <div className="form-group">
            <label>비밀번호</label>
            <input
              type="password"
              placeholder="비밀번호를 입력하세요"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="input-field"
            />
          </div>

          <div className="form-group">
            <label>비밀번호 확인</label>
            <input
              type="password"
              placeholder="비밀번호를 다시 입력하세요"
              value={confirmPassword}
              onChange={(e) => handleConfirmPasswordChange(e.target.value)}
              className="input-field"
            />
            {passwordError && (
              <p className="error-message" style={{ color: "red" }}>
                {passwordError}
              </p>
            )}
          </div>

          <div className="form-group">
            <label>이메일</label>
            <div className="input-row">
              <input
                type="email"
                placeholder="이메일을 입력하세요"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="input-field"
              />
              <button
                type="button"
                className="check-button"
                onClick={handleEmailVerification}
              >
                인증 요청
              </button>
            </div>
          </div>

          <div className="form-group">
            <label>인증번호</label>
            <div className="input-row">
              <input
                type="text"
                placeholder="인증번호를 입력하세요"
                value={verificationCode}
                onChange={(e) => setVerificationCode(e.target.value)}
                className="input-field"
              />
              <button
                type="button"
                className="check-button"
                onClick={handleVerificationCodeCheck}
              >
                인증 확인
              </button>
            </div>
          </div>

          <div className="form-group">
            <label>이름</label>
            <input
              type="text"
              placeholder="이름을 입력하세요"
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="input-field"
            />
          </div>

          <div className="form-group">
            <label>휴대폰 번호</label>
            <input
              type="text"
              placeholder="휴대폰 번호를 입력하세요"
              value={phone}
              onChange={(e) => setPhone(e.target.value)}
              className="input-field"
            />
          </div>

          <button type="submit" className="submit-button">
            회원가입
          </button>
        </form>
      </div>
    </div>
  );
};

export default Register;