import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import TopNav from "./components/Header";
import Footer from "./components/Footer";
import Home from "./pages/Home/Home";
import ChatBot from "./pages/Product/ChatBot";
import Board from "./pages/Service/Board";
import FAQ from "./pages/Service/FAQ";
import Login from "./pages/Login/Login";
import Register from "./pages/Register/Register";
import MyPage from "./pages/User/MyPage";
import FindID from "./pages/Login/FindId";
import FindPassword from "./pages/Login/FindPassword";

function App() {
  return (
    <Router>
      <div style={styles.container}>
        <TopNav />
        <div style={styles.pageContent}>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/Product/ChatBot" element={<ChatBot />} />
            <Route path="/service/board" element={<Board />} />
            <Route path="/service/faq" element={<FAQ />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/mypage" element={<MyPage />} />
            <Route path="/FindId" element={<FindID />} />
            <Route path="/FindPassword" element={<FindPassword />} />
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
  },
  pageContent: {
    flex: 1,
    display: "flex",
    flexDirection: "column",
    marginTop: "60px", // 헤더 높이만큼 여백 추가
  },
};

export default App;