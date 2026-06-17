package com.jasonwu.news_dispatcher.controller;

import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.jasonwu.news_dispatcher.model.DispatchRequest;
import com.jasonwu.news_dispatcher.service.DispatcherService;
@CrossOrigin(origins = "*")
@RestController
@RequestMapping(value ="/app/v1")
public class DispatcherController {
    private DispatcherService dispatcherService;
    public DispatcherController(DispatcherService dispatcherService){
        this.dispatcherService = dispatcherService;
    }
    @PostMapping(consumes = "application/json")
    public String receiveAndDispatcher(@RequestBody DispatchRequest req){
        System.out.println("收到新的通報，準備從資料庫撈取客戶名單並群發...");
        dispatcherService.sendToAllCustomer(req.getHtml());
        return"通報已成功進入群發序列！";
    }
}
