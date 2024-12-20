package com.example.FinalPJ.dto.response.board;

import com.example.FinalPJ.common.ResponseCode;
import com.example.FinalPJ.common.ResponseMessage;
import com.example.FinalPJ.dto.response.ResponseDTO;
import lombok.Getter;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;

@Getter
public class BoardResponseDTO extends ResponseDTO{
    private BoardResponseDTO () {
        super();
    }

    public static ResponseEntity<BoardResponseDTO> success(){
        BoardResponseDTO responsebody = new BoardResponseDTO();
        return ResponseEntity.status(HttpStatus.OK).body(responsebody);
    }

    public static ResponseEntity<ResponseDTO> titleSizeFail() {
        ResponseDTO responsebody = new ResponseDTO(ResponseCode.TITLE_SIZE_ERROR, ResponseMessage.TITLE_SIZE_FAIL);
        return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(responsebody);
    }

    public static ResponseEntity<ResponseDTO> contentSizeFail() {
        ResponseDTO responsebody = new ResponseDTO(ResponseCode.CONTENT_SIZE_ERROR, ResponseMessage.CONTENT_SIZE_FAIL);
        return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(responsebody);
    }

    public static ResponseEntity<ResponseDTO> writerSizeFail() {
        ResponseDTO responsebody = new ResponseDTO(ResponseCode.WRITER_SIZE_ERROR, ResponseMessage.WRITER_SIZE_FAIL);
        return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(responsebody);
    }
}

