import React, { useState } from "react";
import "./FindAccount.css";

const FindPassword = () => {
  const [email, setEmail] = useState("");
  const [verificationSent, setVerificationSent] = useState(false);

  const handleSendVerification = () => {
    // 백엔드 API 연동을 위한 함수 (추후 수정 필요)
    if (email) {
      setVerificationSent(true); // 예시로 인증 메일 전송 상태 변경
    }
  };

  return (
    <div className="find-account-container">
      <h2 className="title">비밀번호 찾기</h2>
      <div className="form-group">
        <label>이메일</label>
        <input
          type="email"
          placeholder="이메일을 입력하세요"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
      </div>
      <button onClick={handleSendVerification}>인증 메일 보내기</button>

      {verificationSent && (
        <div className="result">
          <p>입력하신 이메일로 비밀번호 재설정 링크를 보냈습니다.</p>
        </div>
      )}
    </div>
  );
};

export default FindPassword;