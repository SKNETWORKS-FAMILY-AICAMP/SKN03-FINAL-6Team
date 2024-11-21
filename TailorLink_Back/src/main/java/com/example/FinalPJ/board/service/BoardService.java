package com.example.FinalPJ.board.service;

import com.example.FinalPJ.board.controller.entity.Board;
import com.example.FinalPJ.board.repository.BoardRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import java.time.LocalDateTime;

import java.util.List;

@Service
public class BoardService {

    @Autowired
    private BoardRepository boardRepository;

    // 글 작성 처리
    public void write(Board board) {
        if (board.getCreatetime() == null) {
            board.setCreatetime(LocalDateTime.now()); // 현재 시간 설정
        }

        boardRepository.save(board);
    }

    // 게시글 리스트 처리
    public List<Board> boardList() {
        return boardRepository.findAll();
    }

    // 특정 게시글 불러오기
    public Board boardView(Integer board_id) {

        return boardRepository.findById(board_id).get();

    }

    // 특정 게시글 삭제
    public void boardDelete(Integer board_id) {

        boardRepository.deleteById(board_id);
    }
}
