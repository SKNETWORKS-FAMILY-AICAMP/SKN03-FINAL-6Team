// Board.js
import React, { useState } from 'react';
import { Link } from 'react-router-dom'; // Link 임포트
import './Board.css';

const Board = () => {
  const [posts, setPosts] = useState([
    { id: 1, author: '조내링', title: '야 문거누', content: 'ㅇㅇ' },
    { id: 2, author: '최연규', title: '두 번째 글', content: 'ㅇㅇ' },
    { id: 3, author: '박지용', title: '세 번째 글', content: 'ㅇㅇ' },
    { id: 4, author: '김병수', title: '네 번째 글', content: 'ㅇㅇ' },
    { id: 5, author: '박용주', title: '다섯 번째 글', content: 'ㅇㅇ' },
    { id: 6, author: '조경원', title: '여러분', content: 'ㅇㅇ' },
  ]);

  const [searchText, setSearchText] = useState('');

  // 글쓰기 모달 상태
  const [isWriteModalOpen, setIsWriteModalOpen] = useState(false);
  const [writeForm, setWriteForm] = useState({author:'', title:'', content:''});

  // 수정 모달 상태
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [editForm, setEditForm] = useState({id:null, author:'', title:'', content:''});

  // 삭제 확인 모달 상태
  const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false);
  const [deleteTargetId, setDeleteTargetId] = useState(null);

  // 페이지네이션 상태
  const [currentPage, setCurrentPage] = useState(1);
  const perPage = 5; // 페이지당 표시할 게시글 수

  const filteredPosts = posts.filter(post =>
    post.title.includes(searchText) || post.author.includes(searchText)
  );

  const totalPages = Math.ceil(filteredPosts.length / perPage);
  const startIndex = (currentPage - 1) * perPage;
  const displayedPosts = filteredPosts.slice(startIndex, startIndex + perPage);

  const handleDelete = (id) => {
    setDeleteTargetId(id);
    setIsDeleteModalOpen(true);
  };

  const confirmDelete = () => {
    setPosts(prev => prev.filter(p => p.id !== deleteTargetId));
    setIsDeleteModalOpen(false);
    setDeleteTargetId(null);

    const newTotalPages = Math.ceil((filteredPosts.length - 1)/perPage);
    if(currentPage > newTotalPages && newTotalPages >= 1) {
      setCurrentPage(newTotalPages);
    }
  };

  const handleEdit = (post) => {
    setEditForm({...post});
    setIsEditModalOpen(true);
  };

  const handleWrite = () => {
    // 글쓰기 모달 열기
    setWriteForm({author:'', title:'', content:''});
    setIsWriteModalOpen(true);
  };

  const submitWrite = () => {
    const newId = posts.length > 0 ? Math.max(...posts.map(p=>p.id))+1 : 1;
    const newPost = {
      id: newId,
      author: writeForm.author,
      title: writeForm.title,
      content: writeForm.content
    };
    setPosts([...posts, newPost]);
    setIsWriteModalOpen(false);

    const newTotalPages = Math.ceil((posts.length+1)/perPage);
    setCurrentPage(newTotalPages);
  };

  const submitEdit = () => {
    setPosts(prev =>
      prev.map(p => p.id === editForm.id ? {...p, author: editForm.author, title: editForm.title, content: editForm.content} : p)
    );
    setIsEditModalOpen(false);
  };

  const goToPrevPage = () => {
    if(currentPage > 1) {
      setCurrentPage(currentPage-1);
    }
  };

  const goToNextPage = () => {
    if(currentPage < totalPages) {
      setCurrentPage(currentPage+1);
    }
  };

  return (
    <div className="board-container">
      <aside className="board-sidebar">
        <button className="write-btn" onClick={handleWrite}>글쓰기</button>
        <ul className="menu-list">
          <li><Link to="/service/board" className="sidebar-link">전체 게시판</Link></li>
          <li><Link to="/service/qna" className="sidebar-link">1:1 문의하기</Link></li>
          <li><Link to="/service/faq" className="sidebar-link">FAQ</Link></li>
        </ul>
      </aside>
      <main className="board-main">
        <h2 className="board-title">게시판</h2>
        <div className="board-search">
          <input
            type="text"
            placeholder="검색"
            value={searchText}
            onChange={e => setSearchText(e.target.value)}
          />
          <button>🔍</button>
        </div>
        <div className="board-list">
          {displayedPosts.map((post) => (
            <div key={post.id} className="board-item">
              <div className="board-item-content">
                <div className="board-item-info">
                  <p>글 번호 : {post.id < 10 ? `0${post.id}` : post.id}</p>
                  <p>작성자 : {post.author}</p>
                </div>
                <div className="board-item-body">
                  <p>제목 : {post.title}</p>
                  <p>본문 : {post.content}</p>
                </div>
              </div>
              <div className="board-item-actions">
                <button onClick={() => handleDelete(post.id)}>삭제</button>
                <button onClick={() => handleEdit(post)}>수정</button>
              </div>
            </div>
          ))}
          {filteredPosts.length === 0 && <p>게시글이 없습니다.</p>}
        </div>
        {/* 페이지네이션 버튼 */}
        <div className="pagination">
          <button onClick={goToPrevPage} disabled={currentPage === 1}>이전</button>
          <span>{currentPage} / {totalPages === 0 ? 1 : totalPages}</span>
          <button onClick={goToNextPage} disabled={currentPage === totalPages || totalPages===0}>다음</button>
        </div>
      </main>

      {/* 글쓰기 모달 */}
      {isWriteModalOpen && (
        <div className="modal-overlay">
          <div className="modal-content">
            <h2>글쓰기</h2>
            <div className="form-group">
              <label>작성자</label>
              <input type="text"
                placeholder="이름을 입력하세요"
                value={writeForm.author}
                onChange={e=>setWriteForm({...writeForm, author:e.target.value})}/>
            </div>
            <div className="form-group">
              <label>제목</label>
              <input type="text"
                placeholder="제목을 입력하세요"
                value={writeForm.title}
                onChange={e=>setWriteForm({...writeForm, title:e.target.value})}/>
            </div>
            <div className="form-group">
              <label>내용</label>
              <textarea
                placeholder="내용을 입력하세요"
                value={writeForm.content}
                onChange={e=>setWriteForm({...writeForm, content:e.target.value})}></textarea>
            </div>
            <div className="modal-buttons">
              <button onClick={submitWrite}>등록하기</button>
              <button onClick={()=>setIsWriteModalOpen(false)}>취소</button>
            </div>
          </div>
        </div>
      )}

      {/* 수정 모달 */}
      {isEditModalOpen && (
        <div className="modal-overlay">
          <div className="modal-content">
            <h2>글 수정</h2>
            <div className="form-group">
              <label>작성자</label>
              <input type="text"
                placeholder="이름을 입력하세요"
                value={editForm.author}
                onChange={e=>setEditForm({...editForm, author:e.target.value})}/>
            </div>
            <div className="form-group">
              <label>제목</label>
              <input type="text"
                placeholder="제목을 입력하세요"
                value={editForm.title}
                onChange={e=>setEditForm({...editForm, title:e.target.value})}/>
            </div>
            <div className="form-group">
              <label>내용</label>
              <textarea
                placeholder="내용을 입력하세요"
                value={editForm.content}
                onChange={e=>setEditForm({...editForm, content:e.target.value})}></textarea>
            </div>
            <div className="modal-buttons">
              <button onClick={submitEdit}>등록하기</button>
              <button onClick={()=>setIsEditModalOpen(false)}>취소</button>
            </div>
          </div>
        </div>
      )}

      {/* 삭제 확인 모달 */}
      {isDeleteModalOpen && (
        <div className="modal-overlay">
          <div className="modal-content">
            <h2>선택한 게시물을 정말 삭제하시겠습니까?</h2>
            <p>한번 삭제한 자료는 복구할 수 없습니다.</p>
            <div className="modal-buttons">
              <button onClick={confirmDelete}>삭제</button>
              <button onClick={()=>setIsDeleteModalOpen(false)}>취소</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Board;
