package com.example.FinalPJ.board.dto;

import com.fasterxml.jackson.annotation.JsonFormat;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.Size;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class BoardDTO {
    private Integer board_id;

    @NotNull(message = "제목을 입력해주세요.")
    private String title;

    @NotNull(message = "내용을 입력해주세요.")
    @Size(min = 1, max = 100)
    private String content;

    @NotNull(message = "작성자를 입력해주세요.")
    private String author;

    @JsonFormat(shape = JsonFormat.Shape.STRING, pattern = "yyyy-MM-dd HH:mm:ss")
    private LocalDateTime createtime;
}