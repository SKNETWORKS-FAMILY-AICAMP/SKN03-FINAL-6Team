import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import TopNav from "./components/Header"; // 네비게이션
import Footer from "./components/Footer"; // 푸터
import Home from "./pages/Home/Home"; // 홈
import Features from "./pages/Features/Features"; // 주요 기능
import ContactUs from "./pages/Service/ContactUs"; // 문의하기
import Board from "./pages/Service/Board"; // 게시판
import Login from "./pages/Login/Login"; // 로그인
import Register from "./pages/Register/Register"; // 회원가입
import ScrollToTop from "./components/ScrollToTop"; // 최상단으로 이동 버튼

function App() {
  return (
    <Router>
      <div style={styles.container}>
        <TopNav />
        <ScrollToTop />
        <div style={styles.pageContent}>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/features" element={<Features />} />
            <Route path="/service/contactus" element={<ContactUs />} />
            <Route path="/service/board" element={<Board />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
          </Routes>
        </div>
        <Footer />
      </div>
    </Router>
  );
}

const styles = {
  container: {
    display: "flex",
    flexDirection: "column",
    minHeight: "100vh",
    backgroundColor: "#f0f8ff",
    paddingTop: "59px", // 헤더 높이만큼 여백 추가
  },
  pageContent: {
    flex: 1,
    width: "100%",
    boxSizing: "border-box",
  },
};

export default App;