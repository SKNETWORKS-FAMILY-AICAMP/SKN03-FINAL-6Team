package com.example.FinalPJ.contoroller;

import com.example.FinalPJ.dto.request.auth.*;
import com.example.FinalPJ.dto.response.SignUpResponseDTO;
import com.example.FinalPJ.dto.response.auth.CheckCertificationResponseDTO;
import com.example.FinalPJ.dto.response.auth.EmailCertificationResponseDTO;
import com.example.FinalPJ.dto.response.auth.IdCheckResponseDTO;
import com.example.FinalPJ.dto.response.auth.SignInResponseDTO;
import com.example.FinalPJ.service.AuthService;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.servlet.http.HttpSession;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;


@RestController
@RequestMapping("/v1/auth")
@RequiredArgsConstructor
public class AuthController {
    private final AuthService authService;

    @PostMapping("/id-check")
    public ResponseEntity<? super IdCheckResponseDTO> idCheck(
            @RequestBody @Valid IdCheckRequestDTO requestbody
    ) {
        ResponseEntity<? super IdCheckResponseDTO> response = authService.idCheck(requestbody);
        return response;
    }

    @PostMapping("/email-certification")
    public ResponseEntity<? super EmailCertificationResponseDTO> emailCertification(
            @RequestBody @Valid EmailCertificationRequestDTO requestbody
    ) {
        ResponseEntity<? super EmailCertificationResponseDTO> response = authService.emailCertification(requestbody);
        return response;
    }

    @PostMapping("/check-certification")
    public ResponseEntity<? super CheckCertificationResponseDTO> checkCertification(
            @RequestBody @Valid CheckCertificationRequestDTO requestbody
    ) {
        ResponseEntity<? super CheckCertificationResponseDTO> response = authService.checkCertification(requestbody);
        return response;
    }

    @PostMapping("/sign-up")
    public ResponseEntity<? super SignUpResponseDTO> signUp(
            @RequestBody @Valid SignUpRequestDTO requestbody
    ) {
        ResponseEntity<? super SignUpResponseDTO> response = authService.signUp(requestbody);
        return response;
    }

    @PostMapping("/sign-in")
    public ResponseEntity<? super SignInResponseDTO> signIn(
            @RequestBody @Valid SignInRequestDTO requestbody
    ) {
        ResponseEntity<? super SignInResponseDTO> response = authService.signIn(requestbody);
        return response;
    }

    @GetMapping("/sign-out")
    public String signOut(HttpServletRequest request, HttpServletResponse response) {
        HttpSession session = request.getSession(false);
        if (session != null) {
            session.invalidate(); // 세션 무효화
        }
        return "redirect:/v1/auth/sign-in";
    }
}
