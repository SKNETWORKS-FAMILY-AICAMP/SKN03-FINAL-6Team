package com.example.FinalPJ.dto.response.user;

import com.example.FinalPJ.common.ResponseCode;
import com.example.FinalPJ.common.ResponseMessage;
import com.example.FinalPJ.dto.response.ResponseDTO;
import lombok.Getter;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;

@Getter
public class UserResponseDTO extends ResponseDTO {
    private UserResponseDTO() {
        super();
    }

    public static ResponseEntity<UserResponseDTO> success() {
        UserResponseDTO responsebody = new UserResponseDTO();
        return ResponseEntity.status(HttpStatus.OK).body(responsebody);
    }

    public static ResponseEntity<ResponseDTO> notFoundId() {
        ResponseDTO responsebody = new ResponseDTO(ResponseCode.ID_NOT_FOUND, ResponseMessage.ID_NOT_FOUND);
        return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(responsebody);
    }
}


