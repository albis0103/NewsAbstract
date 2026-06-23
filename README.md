# SecOps News-digest

## Overview
In a modern SOC (Security Operations Center), analysts are overwhelmed by daily security news. This project automates the "News-to-Impact" pipeline by integrating automated summarization, semantic correlation, and prioritized reporting to reduce Mean Time to Acknowledge (MTTA).

### Core Components
1. **SecOps News Analyzer (Python & n8n)**: Extracts core technical values using LLMs and matches news keywords with customer profiles via Word2Vec cosine similarity.
2. **Security News Dispatcher (Java Spring Boot)**: Fetches client lists from MongoDB and dispatches real-time threat notifications via Email (SMTP) and Teams Webhook.

---

### Prerequisites
* **Docker Desktop** (or Docker Engine + Docker Compose)<br>
[solution of installation Trouble on Windows](https://github.com/albis0103/NewsAbstract/wiki/Troubleshooting-&-FAQ)
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

Configure your database and SMTP (e.g., Mailtrap)<br>
:(news-dispatcher-service/src/main/resources/application.properties)
```
spring.data.mongodb.uri=mongodb+srv://<user>:<password>@cluster0.net/SecOpsDB
spring.mail.host=sandbox.smtp.mailtrap.io
spring.mail.port=2525
```
### Step 2: One-Click Deployment

Open your terminal at the root of the project (where docker-compose.yml is located) and run:<br>

Bash<br>
```
docker compose up -d --build
```
Note: The first startup will take a few minutes as it downloads base images and builds the services. Ensure the Word2Vec model (`fast_model.kv`) exists under `news-analyzer-py/models/`.<br>

### Step 3: Initialize n8n Workflow

Once all containers are running, visit http://localhost:5678 to access the n8n dashboard.<br>

Complete the initial setup (create a local admin account).<br>

Import the my_workflow.json (or main-workflow.json) file into n8n.<br>

- Open the **Webhook** node, ensure it listens for **GET** requests, and set **Respond** to **Using Respond to Webhook Node**.
- Verify the flow is: `Webhook → API:digest → API:similarity → Respond to Webhook`, where Respond to Webhook returns JSON (`data` + `similarity`).
- **Activate** the workflow (toggle to active) so the production webhook stays live.<br>

Toggle the workflow to Public.<br>

### Step 4: Launch the UI

Visit `http://localhost:80` in your browser. Click a news card to analyze it, edit the generated digest, and add up to three articles to the weekly report. Preview the rendered email, then dispatch to all matched customers.<br>



## 📚 Documentation (Wiki)
For advanced configurations, architecture logic, and debugging, please visit our Wiki:
* [System Architecture & Workflow](https://github.com/albis0103/NewsAbstract/wiki/System-Architecture-&-Documentation)
* [news-analyzer](https://github.com/albis0103/NewsAbstract/wiki/news%E2%80%90analyzer-Architecture-&-Documentation-(Python-Core-Engine))
* [news-dispatcher](https://github.com/albis0103/NewsAbstract/wiki/news%E2%80%90dispatcher-Architecture-and-Overview-(Java-Dispatch-Backend))
* [Troubleshooting & FAQ](https://github.com/albis0103/NewsAbstract/wiki/Troubleshooting-&-FAQ)
