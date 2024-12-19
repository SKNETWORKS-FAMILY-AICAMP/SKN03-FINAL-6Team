package com.example.tailorlink.entity;

import com.example.tailorlink.dto.request.auth.SignUpRequestDTO;
import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Entity(name = "user")
@Table(name = "user")
public class UserEntity {
    @Id
    private String userId;
    private String password;
    private String name;
    private String email;
    private String phoneNumber;
    private String role;
    private String type;

    public UserEntity(SignUpRequestDTO dto) {
        this.userId = dto.getId();
        this.password = dto.getPassword();
        this.email = dto.getEmail();
        this.name = dto.getName();
        this.phoneNumber = dto.getPhoneNumber();
        this.type = "app";
        this.role = "ROLE_USER";
    }

    public UserEntity (String userId, String email, String type) {
        this.userId = userId;
        this.password = "Password";
        this.email = email;
        this.name = userId;
        this.phoneNumber = null;
        this.type = type;
        this.role = "ROLE_USER";
    }
}