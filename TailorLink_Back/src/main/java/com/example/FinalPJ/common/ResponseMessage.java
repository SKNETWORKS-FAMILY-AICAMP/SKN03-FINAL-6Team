package com.example.FinalPJ.common;

public interface ResponseMessage {
    String SUCCESS = "Success";
    String VAILDATION_FAIL = "Validation Failed";
    String DUPLICATE_ID = "Duplicate ID";
    String SIGN_IN_FAIL = "Login informaion mismatch";
    String CERTIFICATION_FAIL = "Certification Failed";
    String DATABASE_ERROR = "Database Error";
    String MAIL_FAIL = "Mail Send Failed";
    String BAD_REQUEST = "Bad Request";

    String TITLE_SIZE_FAIL = "Title must be between 1 and 30 characters.";
    String CONTENT_SIZE_FAIL = "Content must be at least 10 characters and no more than 300 characters.";
    String WRITER_SIZE_FAIL = "Author must be at least 1 character.";
}
