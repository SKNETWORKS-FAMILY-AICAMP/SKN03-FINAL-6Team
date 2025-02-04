package com.example.FinalPJ.dto.response;

import lombok.AllArgsConstructor;
import lombok.Getter;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;

import com.example.FinalPJ.common.ResponseCode;
import com.example.FinalPJ.common.ResponseMessage;

@Getter
@AllArgsConstructor
public class ResponseDTO {
    private String code;
    private String message;

    public ResponseDTO(){
        this.code = ResponseCode.SUCCESS;
        this.message = ResponseMessage.SUCCESS;
    }

    public static ResponseEntity<ResponseDTO> databaseError(){
        ResponseDTO responseBody = new ResponseDTO(ResponseCode.DATABASE_ERROR, ResponseMessage.DATABASE_ERROR);
        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(responseBody);
    }

    public static ResponseEntity<ResponseDTO> validationFail(){
        ResponseDTO responseBody = new ResponseDTO(ResponseCode.VAILDATION_FAIL, ResponseMessage.VAILDATION_FAIL);
        return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(responseBody);
    }
}
