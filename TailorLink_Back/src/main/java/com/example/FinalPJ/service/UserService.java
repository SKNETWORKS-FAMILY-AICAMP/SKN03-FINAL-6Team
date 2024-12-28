package com.example.FinalPJ.service;

import com.example.FinalPJ.dto.UserDTO;
import com.example.FinalPJ.dto.request.user.PatchUserRequestDTO;
import com.example.FinalPJ.dto.request.user.UserRequestDTO;
import com.example.FinalPJ.dto.response.user.PatchUserResponseDTO;
import com.example.FinalPJ.dto.response.user.UserResponseDTO;
import com.example.FinalPJ.entity.UserEntity;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;

import java.util.Optional;

@Service
public interface UserService {
    void save(UserDTO userDTO);
    Optional<UserEntity> findUserByNameAndEmail(String name, String email);
    ResponseEntity<? super UserResponseDTO> notFoundId(UserRequestDTO dto);
    ResponseEntity<? super PatchUserResponseDTO> patchUser(PatchUserRequestDTO dto, String userId);
}
