package com.jasonwu.news_dispatcher.service;

import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.HttpEntity;


import java.util.HashMap;
import java.util.List;
import java.util.Map;


import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import com.jasonwu.news_dispatcher.repository.CustomerRepository;
import com.jasonwu.news_dispatcher.model.Customer;

@Service
public class DispatcherService {
    private final CustomerRepository customerRepository;
    private final RestTemplate restTemplate = new RestTemplate();
    public DispatcherService(CustomerRepository customerRepository){
        this.customerRepository = customerRepository;
    }
    public void sentToAllCustomer(String plaintext){
        List<Customer> customers = customerRepository.findAll();
            if(customers.isEmpty()){
                System.out.println("MongoDB目前無顧客webhook url");
                return;
            }
            for(Customer customer : customers){
                try {
                    System.out.println("正在發送到網址: " + customer.getWebhookUrl());
                    Map<String, String> payload = new HashMap<>();
                    HttpHeaders headers = new HttpHeaders();
                    headers.setContentType(MediaType.APPLICATION_JSON);
                    headers.set("User-Agent", "Mozilla/5.0");
                    HttpEntity<Map<String, String>> entity = new HttpEntity<>(payload, headers);
                    restTemplate.postForEntity(customer.getWebhookUrl(), entity, String.class);
                    System.out.println("sended success:" + customer.getName());
                } catch (Exception e) {
                    System.out.println("send" + customer.getName() + "error:" + e.getMessage());
                }
                
            }
        }
    }       
            