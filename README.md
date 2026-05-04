# SecOps News-digest

## Overview
In a modern SOC (Security Operations Center), analysts are overwhelmed by daily security news. This project automates the "News-to-Impact" pipeline by integrating automated summarization, semantic correlation, and prioritized reporting to reduce Mean Time to Acknowledge (MTTA).

### Core Components
1. **SecOps News Analyzer (Python & n8n)**: Extracts core technical values using LLMs and matches news keywords with customer profiles via Word2Vec cosine similarity.
2. **Security News Dispatcher (Java Spring Boot)**: Fetches client lists from MongoDB and dispatches real-time threat notifications via Email (SMTP) and Teams Webhook.

---

### Prerequisites
* **Docker Desktop** (or Docker Engine + Docker Compose)
* **MongoDB Atlas** account (or local MongoDB)
* API Keys for **Gemini** and **Jina**

---

### Step 1: Environment Configuration
Create two `.env` files in their respective service directories.

1. **Python Analyzer (`news-analyzer-py/.env`)**
   ```env
   GEMINI_API_KEY=your_gemini_key_here
   JINA_API_KEY=your_jina_key_here
2. **Java Dispatcher (news-dispatcher-service/src/main/resources/application.properties)**
Configure your MongoDB URl and SMTP credentials here before building.

### Step 2: One-Click Deployment

Open your terminal at the root of the project (where docker-compose.yml is located) and run:<br>

Bash<br>
```
docker compose up -d --build
```
Note: The first startup will take a few minutes as it downloads base images and downloads the Word2Vec model inside the Python container.<br>

### Step 3: Initialize n8n Workflow

Once all containers are running, visit http://localhost:5678 to access the n8n dashboard.<br>

Complete the initial setup (create a local admin account).<br>

Import the my_workflow.json (or main-workflow.json) file into n8n.<br>

Open the first Webhook node and ensure it is set to listen for GET requests and Respond is set to When Last Node Finishes.<br>

Toggle the workflow to Public.<br>

### Step 4: Launch the UI

Visit http://localhost:80 (or the port you defined for Nginx) in your browser. You can now submit news URLs and let the automated pipeline do the rest!<br>



## 📚 Documentation (Wiki)
For advanced configurations, architecture logic, and debugging, please visit our Wiki:
* [System Architecture & Workflow](https://github.com/albis0103/NewsAbstract/wiki/System-Architecture-&-Documentation)
* [news-analyzer](https://github.com/albis0103/NewsAbstract/wiki/news%E2%80%90analyzer-Architecture-&-Documentation-(Python-Core-Engine))
* [news-dispatcher](https://github.com/albis0103/NewsAbstract/wiki/news%E2%80%90dispatcher-Architecture-and-Overview-(Java-Dispatch-Backend))
* [Troubleshooting & FAQ](https://github.com/albis0103/NewsAbstract/wiki/Troubleshooting-&-FAQ)
