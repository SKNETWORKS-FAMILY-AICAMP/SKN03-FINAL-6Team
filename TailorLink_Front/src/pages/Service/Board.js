import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import axiosInstance from "../../API/AxiosInstance";
import "./Board.css";

const Board = () => {
  const [posts, setPosts] = useState([]);
  const [writeForm, setWriteForm] = useState({
    writer: "",
    title: "",
    content: "",
  });
  const [editPostId, setEditPostId] = useState(null);
  const [isWriting, setIsWriting] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [formErrors, setFormErrors] = useState({
    title: "",
    content: "",
  });
  const [errorMessage, setErrorMessage] = useState("");

  const fetchPosts = async () => {
    try {
      const response = await axiosInstance.get("/v1/board/list");
      setPosts(response.data);
    } catch (error) {
      console.error("Failed to fetch posts:", error);
    }
  };

  useEffect(() => {
    fetchPosts();
  }, []);

  const validateForm = () => {
    let isValid = true;

    if (writeForm.title.length < 2) {
      setFormErrors((prev) => ({
        ...prev,
        title: "제목은 2글자 이상이어야 합니다.",
      }));
      isValid = false;
    } else if (writeForm.title.length > 30) {
      setFormErrors((prev) => ({
        ...prev,
        title: "제목은 30글자 이하로 작성해 주세요.",
      }));
      isValid = false;
    } else {
      setFormErrors((prev) => ({ ...prev, title: "" }));
    }

    if (writeForm.content.length < 10) {
      setFormErrors((prev) => ({
        ...prev,
        content: "내용은 10글자 이상이어야 합니다.",
      }));
      isValid = false;
    } else if (writeForm.content.length > 300) {
      setFormErrors((prev) => ({
        ...prev,
        content: "내용은 300글자 이하로 작성해 주세요.",
      }));
      isValid = false;
    } else {
      setFormErrors((prev) => ({ ...prev, content: "" }));
    }

    return isValid;
  };

  const handleDelete = async (board_id) => {
    try {
      await axiosInstance.delete(`/v1/board/delete/${board_id}`);
      fetchPosts();
    } catch (error) {
      console.error("Failed to delete post:", error);
    }
  };

  const handleEditSubmit = async () => {
    if (!editPostId || !validateForm()) return;

    try {
      const response = await axiosInstance.put(`/v1/board/update/${editPostId}`, {
        board_id: editPostId,
        writer: writeForm.writer,
        title: writeForm.title,
        content: writeForm.content,
      });
      fetchPosts();
      setWriteForm({ writer: "", title: "", content: "" });
      setIsEditing(false);
    } catch (error) {
      console.error("Failed to edit post:", error);
    }
  };

  const handleWriteSubmit = async () => {
    if (!validateForm()) return;

    console.log("글쓰기 요청 데이터:", writeForm);

    try {
      const response = await axiosInstance.post(
        "/v1/board/write",
        writeForm,
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );
      console.log("글쓰기 성공 응답:", response.data);
      fetchPosts();
      setWriteForm({ writer: "", title: "", content: "" });
      setIsWriting(false);
      setErrorMessage("");
    } catch (error) {
      const errorMsg =
        error.response?.data?.message || "글쓰기 실패: 요청을 확인해주세요.";
      setErrorMessage(errorMsg);
      console.error("글쓰기 실패:", error.response?.data || error.message);
    }
  };

  const startEdit = (post) => {
    setEditPostId(post.board_id);
    setWriteForm({
      writer: post.writer,
      title: post.title,
      content: post.content,
    });
    setIsEditing(true);
    setIsWriting(false);
  };

  return (
    <div className="board-container">
      <aside className="board-sidebar">
        <button
          className="write-btn"
          onClick={() => {
            setIsWriting(true);
            setIsEditing(false);
            setWriteForm({ writer: "", title: "", content: "" });
          }}
        >
          글쓰기
        </button>
        <ul className="menu-list">
          <li>
            <Link to="/service/board" className="sidebar-link">
              전체 게시판
            </Link>
          </li>
          <li>
            <Link to="/service/faq" className="sidebar-link">
              FAQ
            </Link>
          </li>
        </ul>
      </aside>
      <main className="board-main">
        <h2 className="board-title">게시판</h2>
        {errorMessage && <p className="error-message">{errorMessage}</p>}
        {isWriting || isEditing ? (
          <div className="form-container">
            <h3>{isEditing ? "글 수정" : "글쓰기"}</h3>
            <div className="form-group">
              <label>작성자</label>
              <input
                type="text"
                value={writeForm.writer}
                onChange={(e) =>
                  setWriteForm({ ...writeForm, writer: e.target.value })
                }
              />
            </div>
            <div className="form-group">
              <label>제목</label>
              <input
                type="text"
                value={writeForm.title}
                onChange={(e) => {
                  setWriteForm({ ...writeForm, title: e.target.value });
                  validateForm();
                }}
              />
              {formErrors.title && (
                <p className="error-message">{formErrors.title}</p>
              )}
            </div>
            <div className="form-group">
              <label>내용</label>
              <textarea
                value={writeForm.content}
                onChange={(e) => {
                  setWriteForm({ ...writeForm, content: e.target.value });
                  validateForm();
                }}
              />
              {formErrors.content && (
                <p className="error-message">{formErrors.content}</p>
              )}
            </div>
            <div className="form-buttons">
              <button
                onClick={isEditing ? handleEditSubmit : handleWriteSubmit}
                disabled={formErrors.title || formErrors.content}
              >
                {isEditing ? "수정 완료" : "게시"}
              </button>
              <button
                onClick={() => {
                  setIsWriting(false);
                  setIsEditing(false);
                  setWriteForm({ writer: "", title: "", content: "" });
                  setFormErrors({ title: "", content: "" });
                }}
              >
                취소
              </button>
            </div>
          </div>
        ) : (
          <div className="board-list">
            {posts.map((post) => (
              <div key={post.board_id} className="board-item">
                <div className="board-item-content">
                  <p>제목: {post.title}</p>
                  <p>작성자: {post.writer}</p>
                  <p>내용: {post.content}</p>
                </div>
                <div className="board-item-actions">
                  <button onClick={() => handleDelete(post.board_id)}>
                    삭제
                  </button>
                  <button onClick={() => startEdit(post)}>수정</button>
                </div>
              </div>
            ))}
            {posts.length === 0 && <p>게시글이 없습니다.</p>}
          </div>
        )}
      </main>
    </div>
  );
};

export default Board;