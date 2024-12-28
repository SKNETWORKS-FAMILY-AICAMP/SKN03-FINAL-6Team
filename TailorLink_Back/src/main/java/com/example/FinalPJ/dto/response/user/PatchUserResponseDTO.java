package com.example.FinalPJ.dto.response.user;

import com.example.FinalPJ.common.ResponseCode;
import com.example.FinalPJ.common.ResponseMessage;
import com.example.FinalPJ.dto.response.ResponseDTO;
import lombok.Getter;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;

@Getter
public class PatchUserResponseDTO extends ResponseDTO {
    private PatchUserResponseDTO() {
        super(ResponseCode.SUCCESS, ResponseMessage.SUCCESS);
    }

    public static ResponseEntity<? super PatchUserResponseDTO> success() {
        PatchUserResponseDTO result = new PatchUserResponseDTO();
        return ResponseEntity.status(HttpStatus.OK).body(result);
    }

    public static ResponseEntity<ResponseDTO> noExistUser() {
        ResponseDTO result = new ResponseDTO(ResponseCode.NOT_EXISTED_USER, ResponseMessage.NOT_EXISTED_USER);
        return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(result);
    }

    public static ResponseEntity<ResponseDTO> duplicateEmail() {
        ResponseDTO result = new ResponseDTO(ResponseCode.DUPLICATE_EMAIL, ResponseMessage.DUPLICATE_EMAIL);
        return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(result);
    }
}
