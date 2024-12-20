package com.example.FinalPJ.service.implement;

import com.example.FinalPJ.entity.BoardEntity;
import com.example.FinalPJ.exception.BoardNotFoundException;
import com.example.FinalPJ.dto.BoardDTO;
import com.example.FinalPJ.dto.request.board.BoardRequestDTO;
import com.example.FinalPJ.dto.response.board.BoardResponseDTO;
import com.example.FinalPJ.repository.BoardRepository;
import com.example.FinalPJ.service.BoardService;
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
    public ResponseEntity<? super BoardResponseDTO> boardWrite(BoardRequestDTO dto) {
        BoardEntity board = convertRequestToEntity(dto); // 수정된 메서드 호출
        boardRepository.save(board);
        return BoardResponseDTO.success();
    }

    @Override
    public ResponseEntity<? super BoardResponseDTO> boardUpdate(Integer boardId, BoardRequestDTO dto) {
        BoardEntity board = boardRepository.findById(boardId)
                .orElseThrow(() -> new BoardNotFoundException("게시글을 찾을 수 없습니다. ID: " + boardId));
        board.setTitle(dto.getTitle());
        board.setContent(dto.getContent());
        board.setCreatetime(dto.getCreatetime() == null ? LocalDateTime.now() : dto.getCreatetime());
        boardRepository.save(board);
        return BoardResponseDTO.success();
    }

    @Override
    public ResponseEntity<List<BoardDTO>> boardList() {
        List<BoardDTO> boardList = boardRepository.findAll().stream()
                .map(this::convertEntityToDTO) // 수정된 메서드 호출
                .collect(Collectors.toList());
        return ResponseEntity.ok(boardList);
    }

    @Override
    public ResponseEntity<BoardDTO> boardView(Integer boardId) {
        BoardEntity board = boardRepository.findById(boardId)
                .orElseThrow(() -> new BoardNotFoundException("게시글을 찾을 수 없습니다. ID : " + boardId));
        return ResponseEntity.ok(convertEntityToDTO(board)); // 수정된 메서드 호출
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
                .map(this::convertEntityToDTO) // 수정된 메서드 호출
                .collect(Collectors.toList());
        return ResponseEntity.ok(boardList);
    }

    // BoardRequestDTO를 BoardEntity로 변환하는 메서드
    private BoardEntity convertRequestToEntity(BoardRequestDTO dto) {
        BoardEntity board = new BoardEntity();
        board.setTitle(dto.getTitle());
        board.setContent(dto.getContent());
        board.setAuthor(dto.getAuthor());
        board.setCreatetime(LocalDateTime.now());
        return board;
    }

    // BoardEntity를 BoardDTO로 변환하는 메서드
    private BoardDTO convertEntityToDTO(BoardEntity board) {
        return new BoardDTO(
                board.getBoard_id(),
                board.getTitle(),
                board.getContent(),
                board.getAuthor(),
                board.getCreatetime()
        );
    }
}