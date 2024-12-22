package com.example.FinalPJ.service.implement;

import com.example.FinalPJ.common.CertificationNumber;
import com.example.FinalPJ.entity.CertificationEntity;
import com.example.FinalPJ.entity.UserEntity;
import com.example.FinalPJ.dto.request.auth.*;
import com.example.FinalPJ.dto.response.ResponseDTO;
import com.example.FinalPJ.dto.response.SignUpResponseDTO;
import com.example.FinalPJ.dto.response.auth.CheckCertificationResponseDTO;
import com.example.FinalPJ.dto.response.auth.EmailCertificationResponseDTO;
import com.example.FinalPJ.dto.response.auth.IdCheckResponseDTO;
import com.example.FinalPJ.dto.response.auth.SignInResponseDTO;
import com.example.FinalPJ.provider.EmailProvider;
import com.example.FinalPJ.provider.JwtProvider;
import com.example.FinalPJ.repository.CertificationRepository;
import com.example.FinalPJ.repository.UserRepository;
import com.example.FinalPJ.service.AuthService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class AuthServiceImplement implements AuthService {

    private final UserRepository userRepository;
    private final CertificationRepository certificationRepository;

    private final JwtProvider jwtProvider;
    private final EmailProvider emailProvider;

    private final PasswordEncoder passwordEncoder = new BCryptPasswordEncoder();

    @Override
    public ResponseEntity<? super IdCheckResponseDTO> idCheck(IdCheckRequestDTO dto) {
        try{
            String userId = dto.getId();
            boolean isExistId = userRepository.existsByUserId(userId);
            if (isExistId) return IdCheckResponseDTO.duplicateId();

        } catch (Exception exception) {
                exception.printStackTrace();
                return ResponseDTO.databaseError();
        }

        return IdCheckResponseDTO.success();
    }

    @Override
    public ResponseEntity<? super EmailCertificationResponseDTO> emailCertification(EmailCertificationRequestDTO dto) {
        try {
            String userId = dto.getId();
            String email = dto.getEmail();

            // 존재하는 이메일인지 확인
            boolean isExistId = userRepository.existsByUserId(userId);
            if(isExistId) return EmailCertificationResponseDTO.duplicateId();

            // 인증코드 만들기
            String certificationNumber = CertificationNumber.getCertificationNumber();

            // 메일보내기
            boolean isSuccessed = emailProvider.sendCertificationMail(email, certificationNumber);
            if(!isSuccessed) return EmailCertificationResponseDTO.mailSendFail();

            // 전송 결과
            CertificationEntity certificationEntity = new CertificationEntity(userId, email, certificationNumber);
            certificationRepository.save(certificationEntity);

        } catch (Exception exception) {
                exception.printStackTrace();
                return ResponseDTO.databaseError();
        }
        return EmailCertificationResponseDTO.success();
    }


    @Override
    public ResponseEntity<? super CheckCertificationResponseDTO> checkCertification(CheckCertificationRequestDTO dto) {
        try {

            // 필요 정보 가져오기
            String userId = dto.getId();
            String email = dto.getEmail();
            String certificationNumber = dto.getCertificationNumber();

            CertificationEntity certificationEntity = certificationRepository.findByUserId(userId);
            // certificationEntity가 존재하지 않을 때
            if(certificationEntity == null) return CheckCertificationResponseDTO.certificationFail();

            // 이메일과 인증번호가 일치한지
            boolean isMatched = certificationEntity.getEmail().equals(email) && certificationEntity.getCertificationNumber().equals(certificationNumber);
            if (!isMatched) return CheckCertificationResponseDTO.certificationFail();


        } catch (Exception exception) {
            exception.printStackTrace();
            return ResponseDTO.databaseError();
        }

        return CheckCertificationResponseDTO.success();
    }

    @Override
    public ResponseEntity<? super SignUpResponseDTO> signUp(SignUpRequestDTO dto) {
        try{
            // 존재하는 아이디인지 체크
            String userId = dto.getId();
            boolean isExistId = userRepository.existsByUserId(userId);
            if(isExistId) return SignUpResponseDTO.duplicateId();

            String email = dto.getEmail();
            String certificationNumber = dto.getCertificationNumber();
            CertificationEntity certificationEntity = certificationRepository.findByUserId(userId);

            boolean isMatched = certificationEntity.getEmail().equals(email) && certificationEntity.getCertificationNumber().equals(certificationNumber);
            if(!isMatched) return SignUpResponseDTO.certificationFail();

            // 비밀번호 암호화해서 넘기기
            String password = dto.getPassword();
            String encodedPassword = passwordEncoder.encode(password);
            dto.setPassword(encodedPassword);

            UserEntity userEntity = new UserEntity(dto);
            userRepository.save(userEntity);

            certificationRepository.deleteByUserId(userId);

        } catch (Exception exception) {
            exception.printStackTrace();
            return ResponseDTO.databaseError();
        }
        return SignUpResponseDTO.success();
    }

    @Override
    public ResponseEntity<? super SignInResponseDTO> signIn(SignInRequestDTO dto) {
         String token = null;
         try {

             String userId = dto.getId();
             UserEntity userEntity = userRepository.findByUserId(userId);
             if (userEntity == null) SignInResponseDTO.signInFail();

             String password = dto.getPassword();
             String encodedPassword = userEntity.getPassword();
             boolean isMatched = passwordEncoder.matches(password, encodedPassword);
             if (!isMatched) return SignInResponseDTO.signInFail();

             token = jwtProvider.create(userId);

         } catch (Exception exception) {
             exception.printStackTrace();
             return ResponseDTO.databaseError();
         }
         return SignInResponseDTO.success(token);
    }
}
