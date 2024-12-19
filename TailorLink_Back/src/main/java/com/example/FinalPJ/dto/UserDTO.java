package com.example.FinalPJ.dto;

import lombok.*;

@Getter
@Setter
@NoArgsConstructor
@ToString
@AllArgsConstructor
public class UserDTO {
    private long id;
    private String email;
    private String name;
    private String password;
    private String phoneNumber;
    private String role;
    private String type;
}
