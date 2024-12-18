package com.example.FinalPJ.contoroller;

import com.example.FinalPJ.dto.BoardDTO;
import com.example.FinalPJ.dto.response.board.BoardResponseDTO;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.ui.Model;
import com.example.FinalPJ.service.BoardService;
import org.springframework.beans.factory.annotation.Autowired;
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
    public ResponseEntity<? super BoardResponseDTO> boardWritePro(@RequestBody BoardDTO boardDTO) {
        return boardService.boardWrite(boardDTO);
    }

    @GetMapping("/list")
    public String boardList(Model model) {
        // ResponseEntity에서 데이터 추출
        List<BoardDTO> boardList = boardService.boardList().getBody();
        model.addAttribute("list", boardList); // BoardDTO 리스트를 모델에 추가
        return "boardlist"; // boardlist.html 반환
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

    @PostMapping("/update/{board_id}")
    public String boardUpdate(
            @PathVariable("board_id") Integer board_id,
            @Valid @ModelAttribute BoardDTO boardDTO,
            BindingResult bindingResult
    ) {
        // 유효성 검사 실패 시 에러 처리
        if (bindingResult.hasErrors()) {
            return "boardmodify"; // 수정 페이지로 다시 이동
        }

        // 수정 로직 호출
        boardService.boardUpdate(board_id, boardDTO);

        return "redirect:/v1/board/list";
    }

    @GetMapping("/list/sorted")
    public ResponseEntity<?> boardListSortedByDate() {
        return ResponseEntity.ok(boardService.boardListSortByDate());
    }
}

