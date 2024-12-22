package com.example.FinalPJ.dto;
import lombok.*;

import java.time.LocalDateTime;

@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
@ToString
public class BoardDTO {
    private Integer board_id;
    private String title;
    private String content;
    private String writer;
    private LocalDateTime createtime;
}
