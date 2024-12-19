package com.example.tailorlink.service;

import com.example.tailorlink.dto.UserDTO;
import com.example.tailorlink.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class UserService {
    private final UserRepository userRepositiory;
    public void save(UserDTO userDTO) {
    }
}
