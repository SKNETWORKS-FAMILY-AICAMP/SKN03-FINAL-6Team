package com.example.tailorlink.dto.response.auth;

import com.example.tailorlink.common.ResponseCode;
import com.example.tailorlink.common.ResponseMessage;
import com.example.tailorlink.dto.response.ResponseDTO;
import lombok.Getter;
import org.apache.catalina.connector.Response;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;

@Getter
public class IdCheckResponseDTO extends ResponseDTO {

    private IdCheckResponseDTO(){
        super();
    }

    public static ResponseEntity<IdCheckResponseDTO> success(){
        IdCheckResponseDTO responseBody = new IdCheckResponseDTO();
        return ResponseEntity.status(HttpStatus.OK).body(responseBody);
    }

    public static ResponseEntity<ResponseDTO> duplicateId(){
        ResponseDTO responseBody = new ResponseDTO(ResponseCode.DUPLICATE_ID, ResponseMessage.DUPLICATE_ID);
        return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(responseBody);
    }
}
