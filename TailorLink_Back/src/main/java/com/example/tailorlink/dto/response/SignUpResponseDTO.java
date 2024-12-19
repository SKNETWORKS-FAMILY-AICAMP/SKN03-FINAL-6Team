package com.example.tailorlink.dto.response;

import com.example.tailorlink.common.ResponseCode;
import com.example.tailorlink.common.ResponseMessage;
import lombok.Getter;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;

@Getter
public class SignUpResponseDTO extends ResponseDTO {

    private SignUpResponseDTO(){
        super();
    }

    public static ResponseEntity<SignUpResponseDTO> success(){
        SignUpResponseDTO responseBody = new SignUpResponseDTO();
        return ResponseEntity.status(HttpStatus.OK).body(responseBody);
    }

    public static ResponseEntity<ResponseDTO> duplicateId() {
        ResponseDTO responseBody = new ResponseDTO(ResponseCode.DUPLICATE_ID, ResponseMessage.DUPLICATE_ID);
        return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(responseBody);
    }

    public static ResponseEntity<ResponseDTO> certificationFail() {
        ResponseDTO responseBody = new ResponseDTO(ResponseCode.CERTIFICATION_FAIL, ResponseMessage.CERTIFICATION_FAIL);
        return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body(responseBody);
    }
}