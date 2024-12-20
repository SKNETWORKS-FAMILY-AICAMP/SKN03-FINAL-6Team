package com.example.FinalPJ.contoroller;

import com.example.FinalPJ.dto.BoardDTO;
import com.example.FinalPJ.dto.response.board.BoardResponseDTO;
import com.example.FinalPJ.dto.request.board.BoardRequestDTO;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.ui.Model;
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

    @GetMapping("/write")
    public String boardWriteForm() {
        return "boardwrite";
    }

    @PostMapping("/writepro")
    public ResponseEntity<?> boardWritePro(
            @Valid @RequestBody BoardRequestDTO dto,
            BindingResult bindingResult
    ) {
        // 검증 실패 시 처리
        if (bindingResult.hasErrors()) {
            return handleValidationErrors(bindingResult);
        }
        return boardService.boardWrite(dto);
    }

    @PostMapping("/update/{board_id}")
    public ResponseEntity<?> boardUpdate(
            @PathVariable("board_id") Integer board_id,
            @Valid @RequestBody BoardRequestDTO dto, // 반드시 @Valid와 함께
            BindingResult bindingResult // @Valid 바로 다음에 위치해야 함
    ) {
        if (bindingResult.hasErrors()) {
            return handleValidationErrors(bindingResult); // Validation 에러 처리
        }
        return boardService.boardUpdate(board_id, dto);
    }


    @GetMapping("/list")
    public String boardList(Model model) {
        List<BoardDTO> boardList = boardService.boardList().getBody();
        model.addAttribute("list", boardList);
        return "boardlist";
    }

    @GetMapping("/view")
    public String boardView(Model model, @RequestParam("board_id") Integer board_id) {
        BoardDTO board = boardService.boardView(board_id).getBody();
        model.addAttribute("board", board);
        return "boardview";
    }

    @GetMapping("/delete")
    public String boardDelete(@RequestParam("board_id") Integer board_id) {
        boardService.boardDelete(board_id);
        return "redirect:/v1/board/list";
    }

    @GetMapping("/modify/{board_id}")
    public String boardModify(@PathVariable("board_id") Integer board_id, Model model) {
        BoardDTO board = boardService.boardView(board_id).getBody();
        model.addAttribute("board", board);
        return "boardmodify";
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
        if (bindingResult.hasFieldErrors("author")) {
            return BoardResponseDTO.writerSizeFail();
        }
        return ResponseEntity.badRequest().build();
    }
}

