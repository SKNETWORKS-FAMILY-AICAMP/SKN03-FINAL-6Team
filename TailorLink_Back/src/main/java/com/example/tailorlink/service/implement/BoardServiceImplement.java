package com.example.tailorlink.service.implement;

import com.example.tailorlink.dto.BoardDTO;
import com.example.tailorlink.dto.response.board.BoardResponseDTO;
import com.example.tailorlink.entity.BoardEntity;
import com.example.tailorlink.exception.BoardNotFoundException;
import com.example.tailorlink.repository.BoardRepository;
import com.example.tailorlink.service.BoardService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Sort;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.List;
import java.util.stream.Collectors;

@Service
public class BoardServiceImplement implements BoardService {

    @Autowired
    private BoardRepository boardRepository;

    @Override
    public ResponseEntity<? super BoardResponseDTO> boardWrite(BoardDTO boardDTO) {
        BoardEntity board = convertToEntity(boardDTO);
        boardRepository.save(board);
        return BoardResponseDTO.success();
    }

    @Override
    public ResponseEntity<List<BoardDTO>> boardList() {
        List<BoardDTO> boardList = boardRepository.findAll().stream()
                .map(this::convertToDTO)
                .collect(Collectors.toList());
        return ResponseEntity.ok(boardList);
    }

    @Override
    public ResponseEntity<BoardDTO> boardView(Integer boardId) {
        BoardEntity board = boardRepository.findById(boardId)
                .orElseThrow(() -> new BoardNotFoundException("게시글을 찾을 수 없습니다. ID : " + boardId));
        return ResponseEntity.ok(convertToDTO(board));
    }

    @Override
    public ResponseEntity<BoardResponseDTO> boardDelete(Integer boardId) {
        if (!boardRepository.existsById(boardId)) {
            throw new BoardNotFoundException("삭제할 게시글이 존재하지 않습니다. ID : " + boardId);
        }
        boardRepository.deleteById(boardId);
        return BoardResponseDTO.success();
    }

    @Override
    public ResponseEntity<List<BoardDTO>> boardListSortByDate() {
        List<BoardDTO> boardList = boardRepository.findAll(Sort.by(Sort.Direction.DESC, "createtime"))
                .stream()
                .map(this::convertToDTO)
                .collect(Collectors.toList());
        return ResponseEntity.ok(boardList);
    }

    private BoardEntity convertToEntity(BoardDTO boardDTO) {
        BoardEntity board = new BoardEntity();
        board.setTitle(boardDTO.getTitle());
        board.setContent(boardDTO.getContent());
        board.setAuthor(boardDTO.getAuthor());
        board.setCreatetime(boardDTO.getCreatetime() == null ? LocalDateTime.now() : boardDTO.getCreatetime());
        return board;
    }

    private BoardDTO convertToDTO(BoardEntity board) {
        return new BoardDTO(
                board.getBoard_id(),
                board.getTitle(),
                board.getContent(),
                board.getAuthor(),
                board.getCreatetime()
        );
    }

    @Override
    public ResponseEntity<? super BoardResponseDTO> boardUpdate(Integer boardId, BoardDTO boardDTO) {
        // 1. 해당 ID의 게시글 찾기
        BoardEntity board = boardRepository.findById(boardId)
                .orElseThrow(() -> new BoardNotFoundException("게시글을 찾을 수 없습니다. ID: " + boardId));

        // 2. 기존 게시글 정보를 새로운 데이터로 업데이트
        board.setTitle(boardDTO.getTitle());
        board.setContent(boardDTO.getContent());
        board.setCreatetime(boardDTO.getCreatetime() == null ? LocalDateTime.now() : boardDTO.getCreatetime());

        // 3. 저장
        boardRepository.save(board);

        // 4. 성공 응답 반환
        return BoardResponseDTO.success();
    }
}