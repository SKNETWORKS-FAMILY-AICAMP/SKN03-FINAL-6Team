package com.example.FinalPJ.dto.request.board;

import com.fasterxml.jackson.annotation.JsonFormat;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;

import java.time.LocalDateTime;

public class BoardRequestDTO{
    private Integer board_id;

    @NotNull
    @Size(min = 1, max = 30)
    private String title;

    @NotNull
    @Size(min = 10, max = 300)
    private String content;

    @NotNull
    @Size(min = 1)
    private String author;

    @JsonFormat(shape = JsonFormat.Shape.STRING, pattern = "yyyy-MM-dd HH:mm:ss")
    private LocalDateTime createtime;
}
