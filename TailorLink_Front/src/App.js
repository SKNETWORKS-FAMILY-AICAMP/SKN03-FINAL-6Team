import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import TopNav from "./components/Header";
import Footer from "./components/Footer";
import Home from "./pages/Home/Home";
import ChatBot from "./pages/Product/ChatBot";
import Board from "./pages/Service/Board";
import Qna from "./pages/Service/Qna";
import FAQ from "./pages/Service/FAQ";
import Login from "./pages/Login/Login";
import Register from "./pages/Register/Register";
import TextSection from "./pages/Home/components/TextSection";

function App() {
  return (
    <Router>
      <div style={styles.container}>
        <TopNav />
        <div style={styles.pageContent}>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/text-section" element={<TextSection />} />
            <Route path="/Product/ChatBot" element={<ChatBot />} />
            <Route path="/service/board" element={<Board />} />
            <Route path="/service/qna" element={<Qna />} />
            <Route path="/service/faq" element={<FAQ />} />
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
    paddingTop: "59px",
  },
  pageContent: {
    flex: 1,
    width: "100%",
    boxSizing: "border-box",
  },
};

export default App;
