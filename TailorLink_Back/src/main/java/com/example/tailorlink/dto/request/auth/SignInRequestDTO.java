package com.example.tailorlink.dto.request.auth;

import jakarta.validation.constraints.NotBlank;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Getter
@Setter
@NoArgsConstructor
public class SignInRequestDTO {

    @NotBlank
    private String id;

    @NotBlank
    private String password;
}
