package com.jasonwu.news_dispatcher.model;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;
import java.util.List;
@Document(collection  = "webhooks")
public class Customer {
    @Id
    private String id;
    private String name;
    private String webhookUrl;
    private String email;
    private List<String> feature;
    public List<String> getFeature() {
        return feature;
    }
    public void setFeature(List<String> feature) {
        this.feature = feature;
    }
    public String getEmail() {
        return email;
    }
    public void setEmail(String email) {
        this.email = email;
    }
    // getter and setter
    public String getId() {
        return id;
    }
    public void setId(String id) {
        this.id = id;
    }
    public String getName() {
        return name;
    }
    public void setName(String name) {
        this.name = name;
    }
    public String getWebhookUrl() {
        return webhookUrl;
    }
    public void setWebhookUrl(String webhookUrl) {
        this.webhookUrl = webhookUrl;
    }
}
