package com.example.FinalPJ.contoroller;

import com.example.FinalPJ.common.ResponseCode;
import com.example.FinalPJ.dto.request.user.PatchUserRequestDTO;
import com.example.FinalPJ.dto.response.ResponseDTO;
import com.example.FinalPJ.dto.response.user.PatchUserResponseDTO;
import com.example.FinalPJ.dto.response.user.UserResponseDTO;
import com.example.FinalPJ.entity.UserEntity;
import com.example.FinalPJ.service.UserService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.*;

import java.util.Optional;

@RestController
@RequestMapping("/v1/user")
@RequiredArgsConstructor
public class UserController {
    private final UserService userService;

    @PostMapping("/find-id")
    public ResponseEntity<?> findId(@RequestParam("name") String name, @RequestParam("email") String email) {
        Optional<UserEntity> user = userService.findUserByNameAndEmail(name, email);
        if (user.isPresent()) {
            return ResponseEntity.ok(
                    new ResponseDTO(ResponseCode.SUCCESS, "아이디는: " + user.get().getUserId())
            );
        }
        return UserResponseDTO.notFoundId();
    }

    @PatchMapping("/my-page")
    public ResponseEntity<? super PatchUserResponseDTO> patchUser(@RequestBody @Valid PatchUserRequestDTO requestbody, 
                                                                @AuthenticationPrincipal String userId) {
        ResponseEntity<? super PatchUserResponseDTO> response = userService.patchUser(requestbody, userId);
        return response;
    }
}