package com.example.tailorlink.dto.response.auth;

import com.example.tailorlink.common.ResponseCode;
import com.example.tailorlink.common.ResponseMessage;
import com.example.tailorlink.dto.response.ResponseDTO;
import lombok.Getter;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;

@Getter
public class CheckCertificationResponseDTO extends ResponseDTO {
    private CheckCertificationResponseDTO(){
        super();
    }

    public static ResponseEntity<CheckCertificationResponseDTO> success(){
        CheckCertificationResponseDTO responsebody = new CheckCertificationResponseDTO();
        return ResponseEntity.status(HttpStatus.OK).body(responsebody);
    }

    public static ResponseEntity<ResponseDTO> certificationFail() {
        ResponseDTO responsebody = new ResponseDTO(ResponseCode.CERTIFICATION_FAIL, ResponseMessage.CERTIFICATION_FAIL);
        return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body(responsebody);
    }

}
