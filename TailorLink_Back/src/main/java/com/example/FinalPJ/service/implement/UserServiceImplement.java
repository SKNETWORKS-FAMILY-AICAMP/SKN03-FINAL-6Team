package com.example.FinalPJ.service.implement;

import com.example.FinalPJ.dto.UserDTO;
import com.example.FinalPJ.dto.request.user.UserRequestDTO;
import com.example.FinalPJ.dto.response.user.UserResponseDTO;
import com.example.FinalPJ.entity.UserEntity;
import com.example.FinalPJ.repository.UserRepository;
import com.example.FinalPJ.service.UserService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;

import java.util.Optional;

@Service
@RequiredArgsConstructor
public class UserServiceImplement implements UserService {
    private final UserRepository userRepository;

    @Override
    public void save(UserDTO userDTO) {
        // 저장 로직
    }

    @Override
    public Optional<UserEntity> findUserByNameAndEmail(String name, String email) {
        return userRepository.findByNameAndEmail(name, email);
    }

    @Override
    public ResponseEntity<? super UserResponseDTO> notFoundId(UserRequestDTO dto) {
        return UserResponseDTO.notFoundId();
    }
}