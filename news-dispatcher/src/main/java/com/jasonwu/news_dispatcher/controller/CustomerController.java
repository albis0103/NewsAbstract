package com.jasonwu.news_dispatcher.controller;

import com.jasonwu.news_dispatcher.model.Customer;
import com.jasonwu.news_dispatcher.repository.CustomerRepository;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/webhooks")
public class CustomerController {

    private final CustomerRepository customerRepository;

    // 透過建構子注入 Repository
    public CustomerController(CustomerRepository customerRepository) {
        this.customerRepository = customerRepository;
    }

    // 接收 POST 請求並存入 MongoDB
    @PostMapping
    public String addCustomer(@RequestBody Customer customer) {
        customerRepository.save(customer);
        return "✅ 成功將 [" + customer.getName() + "] 的 Webhook 存入 MongoDB！";
    }
}