import React, { useState, useEffect } from "react";
import axiosInstance from "../../API/AxiosInstance";
import "./MyPage.css";

const MyPage = () => {
  const [isEditing, setIsEditing] = useState(false);
  const [passwordCheck, setPasswordCheck] = useState(false);
  const [password, setPassword] = useState("");
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    phoneNumber: "",
    password: "",
  });

  useEffect(() => {
    authenticateUser();
  }, []);

  const authenticateUser = async () => {
    const token = localStorage.getItem("authToken");
    if (!token) {
      alert("로그인이 필요합니다. 로그인 페이지로 이동합니다.");
      window.location.href = "/login";
      return;
    }
    try {
      await fetchUserData();
    } catch (error) {
      console.error("인증 실패:", error);
      alert("인증 실패: 다시 로그인해주세요.");
      localStorage.removeItem("authToken");
      window.location.href = "/login";
    }
  };

  const fetchUserData = async () => {
    try {
      const response = await axiosInstance.patch(`/v1/user/my-page`);
      setFormData({
        name: response.data.name || "",
        email: response.data.email || "",
        phoneNumber: response.data.phoneNumber || "",
        password: "",
      });
    } catch (error) {
      throw new Error("사용자 정보를 가져오지 못했습니다.");
    }
  };

  const handlePasswordCheck = async () => {
    try {
      const response = await axiosInstance.post(`/v1/auth/check-password`, { password });
      if (response.data.success) {
        setPasswordCheck(true);
        alert("비밀번호 확인 성공.");
      } else {
        alert("비밀번호 불일치.");
      }
    } catch (error) {
      console.error("비밀번호 확인 실패:", error.response?.data || error.message);
      alert("비밀번호 확인 실패: 다시 시도해주세요.");
    }
  };

  const handleSubmit = async () => {
    if (!passwordCheck) {
      alert("비밀번호 확인 필요.");
      return;
    }
    try {
      const updatedData = {
        name: formData.name,
        email: formData.email,
        phoneNumber: formData.phoneNumber,
        password: formData.password || undefined,
      };
      const response = await axiosInstance.patch(`/v1/user/my-page`, updatedData);
      if (response.data.code === "SU") {
        alert("수정 완료!");
        setIsEditing(false);
        setPasswordCheck(false);
        fetchUserData();
      } else {
        alert("수정 실패: 다시 시도해주세요.");
      }
    } catch (error) {
      console.error("수정 실패:", error.response?.data || error.message);
      alert("수정 실패: 다시 시도해주세요.");
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  return (
    <div className="mypage-container">
      <div className="mypage-card">
        <h2 className="mypage-title">내정보</h2>
        <div className="mypage-content">
          {!isEditing || !passwordCheck ? (
            <>
              <p>이름: {formData.name}</p>
              <p>이메일: {formData.email}</p>
              <p>휴대전화번호: {formData.phoneNumber}</p>
              <button onClick={() => setIsEditing(true)}>수정하기</button>
            </>
          ) : (
            <>
              <input
                name="name"
                value={formData.name}
                onChange={handleChange}
                placeholder="이름"
              />
              <input
                name="email"
                value={formData.email}
                onChange={handleChange}
                placeholder="이메일"
              />
              <input
                name="phoneNumber"
                value={formData.phoneNumber}
                onChange={handleChange}
                placeholder="휴대전화번호"
              />
              <input
                type="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                placeholder="새 비밀번호 (선택사항)"
              />
              <div className="button-group">
                <button onClick={handleSubmit}>저장하기</button>
                <button onClick={() => setIsEditing(false)}>나가기</button>
              </div>
            </>
          )}
        </div>
      </div>
      {isEditing && !passwordCheck && (
        <div className="modal">
          <div className="modal-content">
            <h3>비밀번호 확인</h3>
            <input
              type="password"
              placeholder="비밀번호 입력"
              onChange={(e) => setPassword(e.target.value)}
            />
            <div className="button-group">
              <button onClick={handlePasswordCheck}>확인</button>
              <button onClick={() => setIsEditing(false)}>취소</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default MyPage;