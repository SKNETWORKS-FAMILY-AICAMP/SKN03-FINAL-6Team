package com.example.FinalPJ.dto.request.user;

import jakarta.validation.constraints.NotNull;

public class UserRequestDTO {
    @NotNull
    private long id;

    @NotNull
    private String email;

    @NotNull
    private String name;

    @NotNull
    private String password;

    @NotNull
    private String phoneNumber;

    private String role;
    private String type;
}

