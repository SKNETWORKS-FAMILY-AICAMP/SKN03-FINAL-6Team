package com.example.FinalPJ.board.controller;

import org.springframework.ui.Model;
import com.example.FinalPJ.board.dto.BoardDTO; 
import com.example.FinalPJ.board.service.BoardService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.validation.BindingResult;
import jakarta.validation.Valid;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.ModelAttribute;

@Controller
public class BoardController {
    @Autowired
    private BoardService boardService;

    @GetMapping("/board/write")
    public String boardWriteForm() {
        return "boardwrite";
    }

    @PostMapping("board/writepro")
    public String boardWritePro(@Valid @RequestBody BoardDTO boardDTO, BindingResult bindingResult, Model model) {
        if (bindingResult.hasErrors()) {
            System.out.println("Validation Errors: " + bindingResult.getAllErrors());
            model.addAttribute("errors", bindingResult.getAllErrors());
            return "boardwrite";
        }
        
        boardService.boardWrite(boardDTO);
        return "redirect:/board/list";
    }

    @GetMapping("/board/list")
    public String boardList(Model model) {
        model.addAttribute("list", boardService.boardList());
        return "boardlist";
    }

    @GetMapping("/board/view")
    public String boardView(Model model, @RequestParam("board_id") Integer board_id) {
        model.addAttribute("board", boardService.boardView(board_id));
        return "boardview";
    }

    @GetMapping("/board/delete")
    public String boardDelete(@RequestParam("board_id") Integer board_id) {
        boardService.boardDelete(board_id);
        return "redirect:/board/list";
    }

    @GetMapping("/board/modify/{board_id}")
    public String boardModify(@PathVariable("board_id") Integer board_id, Model model) {
        model.addAttribute("board", boardService.boardView(board_id));
        return "redirect:/board/modify/{board_id}";
    }

    @PostMapping("/board/update/{board_id}")
    public String boardUpdate(@PathVariable("board_id") Integer board_id, @Valid @ModelAttribute BoardDTO boardDTO, BindingResult bindingResult) {
        // 유효성 검사 실패 시 에러 처리
        if (bindingResult.hasErrors()) {
            return "boardmodify"; // 수정 페이지로 다시 이동
        }

        BoardDTO boardTemp = boardService.boardView(board_id);

        boardTemp.setTitle(boardDTO.getTitle());
        boardTemp.setContent(boardDTO.getContent());

        boardService.boardWrite(boardTemp);

        return "redirect:/board/list";
    }
}

