package com.example.FinalPJ.service;

import com.example.FinalPJ.dto.request.auth.*;
import com.example.FinalPJ.dto.response.auth.CheckCertificationResponseDTO;
import com.example.FinalPJ.dto.response.auth.EmailCertificationResponseDTO;
import com.example.FinalPJ.dto.response.auth.IdCheckResponseDTO;
import com.example.FinalPJ.dto.response.auth.SignInResponseDTO;
import com.example.FinalPJ.dto.response.auth.SignUpResponseDTO;

import org.springframework.http.ResponseEntity;


public interface AuthService {
    ResponseEntity<? super IdCheckResponseDTO> idCheck(IdCheckRequestDTO dto);
    ResponseEntity<? super EmailCertificationResponseDTO> emailCertification(EmailCertificationRequestDTO dto);
    ResponseEntity<? super CheckCertificationResponseDTO> checkCertification(CheckCertificationRequestDTO dto);
    ResponseEntity<? super SignUpResponseDTO> signUp(SignUpRequestDTO dto);
    ResponseEntity<? super SignInResponseDTO> signIn(SignInRequestDTO dto);
}


