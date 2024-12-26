package com.example.FinalPJ.contoroller;

import com.example.FinalPJ.dto.BoardDTO;
import com.example.FinalPJ.dto.request.board.BoardRequestDTO;
import com.example.FinalPJ.dto.response.board.BoardResponseDTO;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import com.example.FinalPJ.service.BoardService;
import org.springframework.stereotype.Controller;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@Controller
@RequestMapping("/v1/board")
public class BoardController {
    private final BoardService boardService;

    public BoardController(BoardService boardService) {
        this.boardService = boardService;
    }

    @PostMapping("/write")
    public ResponseEntity<?> boardWritePro(@RequestBody @Valid BoardRequestDTO dto, BindingResult bindingResult) {
        if (bindingResult.hasErrors()) {
            return handleValidationErrors(bindingResult); // 유효성 검사 실패 처리
        }
        return boardService.boardWrite(dto); // 성공 시 JSON 형태 응답
    }

    @PutMapping("/update/{board_id}")
    public ResponseEntity<?> boardUpdate(
            @PathVariable("board_id") Integer board_id,
            @RequestBody @Valid BoardRequestDTO dto,
            BindingResult bindingResult
    ) {
        if (bindingResult.hasErrors()) {
            return handleValidationErrors(bindingResult);
        }
        return boardService.boardUpdate(board_id, dto);
    }

    @GetMapping("/list")
    public ResponseEntity<List<BoardDTO>> boardList() {
        return boardService.boardList(); // JSON 형태로 데이터 반환
    }

    @GetMapping("/view/{board_id}")
    public ResponseEntity<BoardDTO> boardView(@PathVariable("board_id") Integer board_id) {
        return boardService.boardView(board_id); // JSON 형태로 반환
    }

    @DeleteMapping("/delete/{board_id}")
    public ResponseEntity<?> boardDelete(@PathVariable("board_id") Integer board_id) {
        boardService.boardDelete(board_id);
        return ResponseEntity.ok().body("게시물이 성공적으로 삭제되었습니다.");
    }

    @PutMapping("/modify/{board_id}")
    public ResponseEntity<?> boardModify(@PathVariable("board_id") Integer board_id, @RequestBody BoardRequestDTO dto) {
        boardService.boardUpdate(board_id, dto);
        return ResponseEntity.ok().body("게시물이 성공적으로 수정되었습니다.");
    }

    @GetMapping("/list/sorted")
    public ResponseEntity<?> boardListSortedByDate() {
        return ResponseEntity.ok(boardService.boardListSortByDate());
    }

    // 공통 검증 에러 처리 메서드
    private ResponseEntity<?> handleValidationErrors(BindingResult bindingResult) {
        if (bindingResult.hasFieldErrors("title")) {
            return BoardResponseDTO.titleSizeFail();
        }
        if (bindingResult.hasFieldErrors("content")) {
            return BoardResponseDTO.contentSizeFail();
        }
        if (bindingResult.hasFieldErrors("writer")) {
            return BoardResponseDTO.writerSizeFail();
        }
        return ResponseEntity.badRequest().build();
    }
}