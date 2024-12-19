package com.example.FinalPJ.common;

public interface ResponseCode {

    String SUCCESS = "SU";
    String VAILDATION_FAIL = "VF";
    String DUPLICATE_ID = "DI";
    String SIGN_IN_FAIL = "SF";
    String CERTIFICATION_FAIL = "CF";
    String DATABASE_ERROR = "DBE";
    String MAIL_FAIL = "MF";
    String BAD_REQUEST = "BR";

    String TITLE_SIZE_ERROR = "VF001"; // 제목 길이 제한 위반
    String CONTENT_SIZE_ERROR = "VF002"; // 내용 길이 제한 위반
    String WRITER_SIZE_ERROR = "VF003"; // 작성자 길이 제한 위반
}
