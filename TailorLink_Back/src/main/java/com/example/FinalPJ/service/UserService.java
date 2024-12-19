package com.example.FinalPJ.service;

import com.example.FinalPJ.dto.UserDTO;
import com.example.FinalPJ.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class UserService {
    private final UserRepository userRepositiory;
    public void save(UserDTO userDTO) {
    }
}
