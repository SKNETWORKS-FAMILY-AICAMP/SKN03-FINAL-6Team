package com.example.FinalPJ.board.service;

import com.example.FinalPJ.board.controller.entity.Board;
import com.example.FinalPJ.board.repository.BoardRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.example.FinalPJ.board.dto.BoardDTO;
import java.util.stream.Collectors;
import java.time.LocalDateTime;

import java.util.List;

@Service
public class BoardService {

    @Autowired
    private BoardRepository boardRepository;

    // 글 작성 처리
    public void boardWrite(BoardDTO boardDTO) {
        Board board = convertToEntity(boardDTO);
        boardRepository.save(board);
    }

    public void boardWrite(Board boardTemp) {
        boardRepository.save(boardTemp);
    }

    // 게시글 리스트 처리
    public List<BoardDTO> boardList() {
        return boardRepository.findAll().stream()
                .map(this::convertToDTO)
                .collect(Collectors.toList());
    }

    // 특정 게시글 불러오기
    public BoardDTO boardView(Integer board_id) {
        Board board = boardRepository.findById(board_id)
                .orElseThrow(() -> new RuntimeException("게시글을 찾을 수 없습니다."));
        return convertToDTO(board);

    }

    // 특정 게시글 삭제
    public void boardDelete(Integer board_id) {
        boardRepository.deleteById(board_id);
    }

    private Board convertToEntity(BoardDTO boardDTO) {
        Board board = new Board();
        board.setTitle(boardDTO.getTitle());
        board.setContent(boardDTO.getContent());
        board.setAuthor(boardDTO.getAuthor());
        board.setCreatetime(boardDTO.getCreatetime() == null ? LocalDateTime.now() : boardDTO.getCreatetime());
        return board;
    }

    private BoardDTO convertToDTO(Board board) {
        return new BoardDTO(
                board.getBoard_id(),
                board.getTitle(),
                board.getContent(),
                board.getAuthor(),
                board.getCreatetime()
        );
    }
}
