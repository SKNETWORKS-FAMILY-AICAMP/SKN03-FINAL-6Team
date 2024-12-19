package com.example.tailorlink.service;

import com.example.tailorlink.dto.BoardDTO;
import com.example.tailorlink.dto.response.board.BoardResponseDTO;
import org.springframework.http.ResponseEntity;

import java.util.List;

public interface BoardService {
    ResponseEntity<? super BoardResponseDTO> boardWrite(BoardDTO boardDTO);
    ResponseEntity<List<BoardDTO>> boardList();
    ResponseEntity<BoardDTO> boardView(Integer boardId);
    ResponseEntity<BoardResponseDTO> boardDelete(Integer boardId);
    ResponseEntity<List<BoardDTO>> boardListSortByDate();
    ResponseEntity<? super BoardResponseDTO> boardUpdate(Integer boardId, BoardDTO boardDTO); // Update 추가
}