package com.example.FinalPJ.board.controller;

import org.springframework.ui.Model;
import com.example.FinalPJ.board.controller.entity.Board;
import com.example.FinalPJ.board.service.BoardService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;

@Controller
public class BoardController {
    @Autowired
    private BoardService boardService;

    @GetMapping("/board/write")
    public String boardWriteForm() {
        return "boardwrite";
    }

    @PostMapping("/board/writepro")
    public String boardWritePro(Board board) {

        boardService.write(board);
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

        return "boardmodify";
    }

    @PostMapping("/board/update/{board_id}")
    public String boardUpdate(@PathVariable("board_id") Integer board_id, Board board) {

        Board boardTemp = boardService.boardView(board_id);

        boardTemp.setTitle(board.getTitle());
        boardTemp.setContent(board.getContent());

        boardService.write(boardTemp);

        return "redirect:/board/list";
    }
}