package com.example.FinalPJ.dto.request.board;

import java.time.LocalDateTime;
import lombok.Data;

@Data
public class BoardRequestDTO {
    private String title;
    private String content;
    private String author;
    private LocalDateTime createtime;
}
