package com.example.tailorlink.service;

import com.example.tailorlink.dto.request.auth.*;
import com.example.tailorlink.dto.response.SignUpResponseDTO;
import com.example.tailorlink.dto.response.auth.CheckCertificationResponseDTO;
import com.example.tailorlink.dto.response.auth.EmailCertificationResponseDTO;
import com.example.tailorlink.dto.response.auth.IdCheckResponseDTO;
import com.example.tailorlink.dto.response.auth.SignInResponseDTO;
import org.springframework.http.ResponseEntity;


public interface AuthService {
    ResponseEntity<? super IdCheckResponseDTO> idCheck(IdCheckRequestDTO dto);
    ResponseEntity<? super EmailCertificationResponseDTO> emailCertification(EmailCertificationRequestDTO dto);
    ResponseEntity<? super CheckCertificationResponseDTO> checkCertification(CheckCertificationRequestDTO dto);
    ResponseEntity<? super SignUpResponseDTO> signUp(SignUpRequestDTO dto);
    ResponseEntity<? super SignInResponseDTO> signIn(SignInRequestDTO dto);
}


