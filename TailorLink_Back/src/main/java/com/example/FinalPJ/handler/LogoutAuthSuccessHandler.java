package com.example.FinalPJ.handler;

import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.security.core.Authentication;
import org.springframework.security.web.authentication.logout.LogoutSuccessHandler;
import org.springframework.stereotype.Component;


import java.io.IOException;

@Component
public class LogoutAuthSuccessHandler implements LogoutSuccessHandler {

    @Override
    public void onLogoutSuccess(HttpServletRequest request, HttpServletResponse response, Authentication authentication) throws IOException {
        // 로그아웃 성공 시 원하는 동작
        response.setStatus(HttpServletResponse.SC_OK);
        response.getWriter().write("Logout successful!");
    }
}