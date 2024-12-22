package com.example.FinalPJ.provider;

import jakarta.mail.internet.MimeMessage;
import lombok.RequiredArgsConstructor;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.mail.javamail.MimeMessageHelper;
import org.springframework.stereotype.Component;

@Component
@RequiredArgsConstructor
public class EmailProvider {

    private final JavaMailSender javamailSender;

    private final String SUBJECT = "[Tailor Link] 인증 메일입니다.";

    public boolean sendCertificationMail(String email, String certificationNumber) {

        try {
            MimeMessage message = javamailSender.createMimeMessage();
            MimeMessageHelper messagehelper = new MimeMessageHelper(message, true);

            String htmlContent = getCertificationMessage(certificationNumber);

            messagehelper.setTo(email);
            messagehelper.setSubject(SUBJECT);
            messagehelper.setText(htmlContent, true);

            javamailSender.send(message);

        } catch (Exception exception) {
            exception.printStackTrace();
            return false;
        }

        return true;
    }

    private String getCertificationMessage(String certificationNumber) {
        String certificationMessage = "";
        certificationMessage += "<h1 style = 'text-align: center;'>[Tailor Link] 인증메일</h1>";
        certificationMessage += "<h3 style = 'text-align: center;'>인증코드 : <strong style = 'font-size:32px; letter-spacing:8px;'>" + certificationNumber + "</strong></h3>";
        return certificationMessage;
    }
}
