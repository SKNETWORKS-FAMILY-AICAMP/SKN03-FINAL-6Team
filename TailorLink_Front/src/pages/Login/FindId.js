import React, { useState } from "react";
import { useNavigate } from "react-router-dom"; // 네비게이션을 위한 훅
import axiosInstance from "../../API/AxiosInstance"; // AxiosInstance를 가져옵니다.
import "./FindAccount.css";

const FindId = () => {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [foundId, setFoundId] = useState(null);
  const [errorMessage, setErrorMessage] = useState("");
  const navigate = useNavigate(); // 네비게이션 훅 사용

  const handleFindId = async () => {
    try {
      const formData = new FormData(); // FormData 객체 생성
      formData.append("name", name.trim());
      formData.append("email", email.trim());

      const response = await axiosInstance.post("/v1/user/find-id", formData, {
        headers: { "Content-Type": "multipart/form-data" }, // 폼 데이터 전송을 명시
      });

      if (response.data && response.data.message) {
        setFoundId(response.data.message);
        setErrorMessage(""); // 에러 메시지를 초기화
      } else {
        setErrorMessage("아이디를 찾을 수 없습니다. 정보를 다시 확인해주세요.");
      }
    } catch (error) {
      const errorMsg =
        error.response?.data?.message || "아이디 찾기에 실패했습니다. 다시 시도해주세요.";
      setErrorMessage(errorMsg);
      setFoundId(null); // 결과를 초기화
    }
  };

  const handleGoToLogin = () => {
    navigate("/login"); // 로그인 페이지로 이동
  };

  return (
    <div className="find-account-container">
      <h2 className="title">아이디 찾기</h2>
      <div className="form-group">
        <label>이름</label>
        <input
          type="string"
          placeholder="이름을 입력하세요"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
      </div>
      <div className="form-group">
        <label>이메일</label>
        <input
          type="string"
          placeholder="이메일을 입력하세요"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
      </div>
      <button onClick={handleFindId}>아이디 찾기</button>

      {errorMessage && (
        <div className="result" style={{ color: "red" }}>
          <p>{errorMessage}</p>
        </div>
      )}

      {foundId && (
        <div className="result">
          <p>
            찾으신 아이디: <strong>{foundId}</strong>
          </p>
          <button onClick={handleGoToLogin} className="login-button">
            로그인하기
          </button>
        </div>
      )}
    </div>
  );
};

export default FindId;