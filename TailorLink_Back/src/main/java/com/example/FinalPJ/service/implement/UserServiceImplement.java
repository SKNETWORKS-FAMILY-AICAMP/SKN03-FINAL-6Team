package com.example.FinalPJ.service.implement;

import com.example.FinalPJ.dto.UserDTO;
import com.example.FinalPJ.dto.request.user.PatchUserRequestDTO;
import com.example.FinalPJ.dto.request.user.UserRequestDTO;
import com.example.FinalPJ.dto.response.ResponseDTO;
import com.example.FinalPJ.dto.response.user.PatchUserResponseDTO;
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
    }

    @Override
    public Optional<UserEntity> findUserByNameAndEmail(String name, String email) {
        return userRepository.findByNameAndEmail(name, email);
    }

    @Override
    public ResponseEntity<? super UserResponseDTO> notFoundId(UserRequestDTO dto) {
        return UserResponseDTO.notFoundId();
    }

    @Override
    public ResponseEntity<? super PatchUserResponseDTO> patchUser(PatchUserRequestDTO dto, String userId) {
        try {
            UserEntity userEntity = userRepository.findByUserId(userId);
            if (userEntity == null) PatchUserResponseDTO.noExistUser();

            String email = dto.getEmail();
            boolean existedEmail = userRepository.existsByEmail(email);
            if (existedEmail) return PatchUserResponseDTO.duplicateEmail();

            String name = dto.getName();
            boolean existedName = userRepository.existsByName(name);
            if (existedName) return PatchUserResponseDTO.success();

            String phoneNumber = dto.getPhoneNumber();
            boolean existedNumber = userRepository.existsByPhoneNumber(phoneNumber);
            if (existedNumber) return PatchUserResponseDTO.success();

            userEntity.setEmail(email);
            userEntity.setName(name);
            userEntity.setPhoneNumber(phoneNumber);
            userRepository.save(userEntity);

        } catch (Exception exception) {
            exception.printStackTrace();
            return ResponseDTO.databaseError();
        }
        return PatchUserResponseDTO.success();
    }
}