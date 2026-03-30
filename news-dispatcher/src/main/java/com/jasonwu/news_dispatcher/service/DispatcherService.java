package com.jasonwu.news_dispatcher.service;

import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;

import java.util.List;


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
            String safetext = plaintext.replace("\"", "\\\"").replace("\n", "\\n");
            String teamsPayload = "{\"text\": \"" + safetext + "\"}";
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            HttpEntity<String> request = new HttpEntity<>(teamsPayload, headers);

            for(Customer customer:customers){
                try {
                    restTemplate.postForObject(customer.getWebhookUrl(), request, String.class);
                    System.out.println("sended success:" + customer.getName());
                } catch (Exception e) {
                    System.out.println("Send:" + customer.getName() + "error:" + e.getMessage());
                }
            }
        }
    }       
            