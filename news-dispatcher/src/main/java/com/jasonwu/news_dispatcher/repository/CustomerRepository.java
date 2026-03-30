package com.jasonwu.news_dispatcher.repository;

import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;
import com.jasonwu.news_dispatcher.model.Customer;

@Repository
public interface CustomerRepository extends MongoRepository<Customer, String> {

    
}
