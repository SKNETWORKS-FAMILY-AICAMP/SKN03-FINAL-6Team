package com.example.tailorlink.dto.response.auth;

import com.example.tailorlink.common.ResponseCode;
import com.example.tailorlink.common.ResponseMessage;
import com.example.tailorlink.dto.response.ResponseDTO;
import com.example.tailorlink.dto.response.SignUpResponseDTO;
import lombok.Getter;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;

@Getter
public class SignInResponseDTO extends ResponseDTO {

    private String token;
    private int expirationTime;

    private SignInResponseDTO (String token) {
        super();
        this.token = token;
        this.expirationTime = 3600;
    }

    public static ResponseEntity<SignInResponseDTO> success (String token) {
        SignInResponseDTO responseBody = new SignInResponseDTO(token);
        return ResponseEntity.status(HttpStatus.OK).body(responseBody);
    }

    public static ResponseEntity<ResponseDTO> signInFail() {
        ResponseDTO responseBody = new ResponseDTO(ResponseCode.SIGN_IN_FAIL, ResponseMessage.SIGN_IN_FAIL);
        return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body(responseBody);
    }

}
