package com.example.tailorlink.contoroller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@Controller
@RequestMapping("/v1")
public class HomeController {
    @GetMapping("/main")
    public String main() {
        return "main";
    }



}
