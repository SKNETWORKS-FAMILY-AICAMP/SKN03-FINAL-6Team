// Qna.js
import React, { useState } from 'react';
import Sidebar from './Sidebar';
import './Qna.css';

const Qna = () => {
  // 문의 목록 상태
  const [qnaPosts, setQnaPosts] = useState([
    { id: 1, author: '박용주', title: '배송 문의', content: '언제 배송되나요?', category: '서비스' },
    { id: 2, author: '박용주', title: '환불 문의', content: '환불은 어떻게 요청하나요?', category: '환불' },
  ]);

  const [qnaWriteForm, setQnaWriteForm] = useState({author:'', title:'', content:'', category:'가격'});
  const [qnaSearchText, setQnaSearchText] = useState('');

  // 페이지네이션 상태
  const [qnaCurrentPage, setQnaCurrentPage] = useState(1);
  const qnaPerPage = 5;

  // 검색 필터링: 제목, 작성자, 카테고리 중 하나라도 검색어 포함 시 필터링
  const qnaFilteredPosts = qnaPosts.filter(post =>
    post.title.includes(qnaSearchText) ||
    post.author.includes(qnaSearchText) ||
    post.category.includes(qnaSearchText)
  );

  const qnaTotalPages = Math.ceil(qnaFilteredPosts.length / qnaPerPage);
  const qnaStartIndex = (qnaCurrentPage - 1) * qnaPerPage;
  const qnaDisplayedPosts = qnaFilteredPosts.slice(qnaStartIndex, qnaStartIndex + qnaPerPage);

  const goToPrevPage = () => {
    if(qnaCurrentPage > 1) {
      setQnaCurrentPage(qnaCurrentPage - 1);
    }
  };

  const goToNextPage = () => {
    if(qnaCurrentPage < qnaTotalPages) {
      setQnaCurrentPage(qnaCurrentPage + 1);
    }
  };

  const submitQna = (e) => {
    e.preventDefault();
    const newId = qnaPosts.length > 0 ? Math.max(...qnaPosts.map(p=>p.id))+1 : 1;
    const newPost = {
      id: newId,
      author: qnaWriteForm.author,
      title: qnaWriteForm.title,
      content: qnaWriteForm.content,
      category: qnaWriteForm.category
    };
    setQnaPosts([...qnaPosts, newPost]);
    setQnaWriteForm({author:'', title:'', content:'', category:'가격'});

    // 새 글 추가 후 마지막 페이지로 이동
    const newTotalPages = Math.ceil((qnaPosts.length+1)/qnaPerPage);
    setQnaCurrentPage(newTotalPages);
  };

  return (
    <div className="board-container">
      <Sidebar /> {/* 글쓰기 버튼 없음 */}
      <div className="board-main">
        <h2 className="board-title">1:1 문의하기</h2>
        <div className="qna-intro">
          <p>궁금하신 사항을 남겨주시면 빠르게 답변하겠습니다.</p>
        </div>
        <div className="board-search">
          <input
            type="text"
            placeholder="검색 (작성자/제목/카테고리)"
            value={qnaSearchText}
            onChange={e => setQnaSearchText(e.target.value)}
          />
          <button>🔍</button>
        </div>
        <div className="qna-form-container">
          <h3>문의 등록</h3>
          <form className="qna-form" onSubmit={submitQna}>
            <div className="form-group">
              <label>작성자</label>
              <input type="text"
                placeholder="이름을 입력하세요"
                value={qnaWriteForm.author}
                onChange={e=>setQnaWriteForm({...qnaWriteForm, author:e.target.value})}/>
            </div>
            <div className="form-group">
              <label>제목</label>
              <input type="text"
                placeholder="제목을 입력하세요"
                value={qnaWriteForm.title}
                onChange={e=>setQnaWriteForm({...qnaWriteForm, title:e.target.value})}/>
            </div>
            <div className="form-group">
              <label>카테고리</label>
              <select
                value={qnaWriteForm.category}
                onChange={e=>setQnaWriteForm({...qnaWriteForm, category:e.target.value})}
                style={{padding:'8px', border:'1px solid #ccc', borderRadius:'5px', fontSize:'14px'}}
              >
                <option value="가격">가격</option>
                <option value="환불">환불</option>
                <option value="고객응대">고객응대</option>
                <option value="서비스">서비스</option>
                <option value="기타">기타</option>
              </select>
            </div>
            <div className="form-group">
              <label>내용</label>
              <textarea
                placeholder="내용을 입력하세요"
                value={qnaWriteForm.content}
                onChange={e=>setQnaWriteForm({...qnaWriteForm, content:e.target.value})}></textarea>
            </div>
            <button type="submit" className="qna-submit-btn">문의 등록</button>
          </form>
        </div>

        <div className="qna-list-section">
          <h3>문의 목록</h3>
          {qnaDisplayedPosts.map(post => (
            <div key={post.id} className="qna-item">
              <div className="qna-item-header">
                <p><strong>작성자:</strong> {post.author}</p>
                <p><strong>제목:</strong> {post.title}</p>
                <p><strong>카테고리:</strong> {post.category}</p>
              </div>
              <div className="qna-item-body">
                <p>{post.content}</p>
              </div>
            </div>
          ))}
          {qnaFilteredPosts.length === 0 && <p>문의가 없습니다.</p>}
        </div>

        {/* 페이지네이션 */}
        <div className="pagination">
          <button onClick={goToPrevPage} disabled={qnaCurrentPage === 1}>이전</button>
          <span>{qnaCurrentPage} / {qnaTotalPages === 0 ? 1 : qnaTotalPages}</span>
          <button onClick={goToNextPage} disabled={qnaCurrentPage === qnaTotalPages || qnaTotalPages===0}>다음</button>
        </div>
      </div>
    </div>
  );
};

export default Qna;
