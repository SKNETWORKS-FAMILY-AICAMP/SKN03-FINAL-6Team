package com.example.tailorlink.dto.response.auth;

import com.example.tailorlink.common.ResponseCode;
import com.example.tailorlink.common.ResponseMessage;
import com.example.tailorlink.dto.response.ResponseDTO;
import lombok.Getter;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;

@Getter
public class EmailCertificationResponseDTO extends ResponseDTO {

    private EmailCertificationResponseDTO() {
        super();
    }

    public static ResponseEntity<EmailCertificationResponseDTO> success() {
        EmailCertificationResponseDTO responsebody = new EmailCertificationResponseDTO();
        return ResponseEntity.status(HttpStatus.OK).body(responsebody);
    }

    public static ResponseEntity<ResponseDTO> duplicateId() {
        ResponseDTO responsebody = new ResponseDTO(ResponseCode.DUPLICATE_ID, ResponseMessage.DUPLICATE_ID);
        return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(responsebody);
    }

    public static ResponseEntity<ResponseDTO> mailSendFail() {
        ResponseDTO responsebody = new ResponseDTO(ResponseCode.MAIL_FAIL, ResponseMessage.MAIL_FAIL);
        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(responsebody);
    }
}
