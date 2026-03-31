package com.jasonwu.news_dispatcher.service;

import java.util.List;

import org.springframework.mail.SimpleMailMessage;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.stereotype.Service;

import com.jasonwu.news_dispatcher.model.Customer;
import com.jasonwu.news_dispatcher.repository.CustomerRepository;

@Service
public class DispatcherService {
    private CustomerRepository customerRepository;
    private final JavaMailSender mailSender;
    public DispatcherService(CustomerRepository customerRepository, JavaMailSender mailSender){
        this.customerRepository = customerRepository;
        this.mailSender = mailSender;
    }



    public void sendToAllCustomer(String plaintext){
        List<Customer> customers = customerRepository.findAll();
        if(customers.isEmpty()){
            System.out.println("MongoDB目前無資料");
            return;
        }
        for(Customer customer : customers){
            if(customer.getEmail() != null && !customer.getEmail().isEmpty()){
                try {
                    System.out.println("preparing send email to :" + customer.getName());
                    SimpleMailMessage message = new SimpleMailMessage();
                    message.setFrom("sandbox.smtp.mailtrap.io");
                    message.setTo(customer.getEmail());
                    message.setSubject("Security News");
                    message.setText(plaintext);
                    mailSender.send(message);
                } catch (Exception e) {
                    System.out.println("send to "+  customer.getName() + "ERROR" + e.getMessage());
                }
            }else{
                System.out.println("跳過 " + customer.getName() + " (未設定 Email)");
            }
        }
        
    }
}       
            