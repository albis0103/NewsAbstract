# SecOps News-digest

## Overview
In a modern SOC (Security Operations Center), analysts are overwhelmed by daily security news. This project automates the "News-to-Impact" pipeline by integrating automated summarization, semantic correlation, and prioritized reporting to reduce Mean Time to Acknowledge (MTTA).

### Core Components
1. **SecOps News Analyzer (Python & n8n)**: Extracts core technical values using LLMs and matches news keywords with customer profiles via Word2Vec cosine similarity.
2. **Security News Dispatcher (Java Spring Boot)**: Fetches client lists from MongoDB and dispatches real-time threat notifications via Email (SMTP) and Teams Webhook.

---

##  Prerequisites
Ensure the following are installed in your environment before proceeding:
* **Python 3.10+**
* **Node.js** (for n8n)
* **Java 17+** & **Maven**
* **MongoDB Atlas** account & **SMTP Server** (e.g., Mailtrap for testing)

---

### Step 1: Initialize Database & Java Server
1. Create a MongoDB collection named `webhooks` and insert your test client data.
2. Configure your database URI and SMTP credentials in `src/main/resources/application.properties`.

### Step 2: Prepare Python Environment & Model
Open a new terminal and set up the analyzer engine:
```powersshell
cd "/[YOUR_PATH]/NewsAbstract/news-analyzer-py"
# Install dependencies
pip install -r requirements.txt
pip install pymongo dnspython

# Initialize Word2Vec model
python keyvector_model.py
```
### Step 3: Configure & Start n8n
In the same terminal, set the required environment variables and launch n8n:<br>
- Windows (PowerShell):<br>
```
$env:GEMINI_API_KEY="YOUR_GEMINI_KEY"
$env:JINA_API_KEY="YOUR_JINA_KEY"
$env:NODES_EXCLUDE="[]"
$env:PYTHONIOENCODING="utf-8"
npx n8n
```
- macOS/Linux:
```
export GEMINI_API_KEY="YOUR_GEMINI_KEY"
export JINA_API_KEY="YOUR_JINA_KEY"
export NODES_EXCLUDE="[]"
export PYTHONIOENCODING="utf-8"
npx n8n
```
### Step 4: Import Workflow & Test
1.Access n8n: Open http://localhost:5678 in your browser.<br>
2.Import: Drag and drop my_workflow.json into the canvas and click Publish.<br>
3.Launch UI: Open Analyzer.html (or webhook.html) in your browser to interact with the system!<br>

## 📚 Documentation (Wiki)
For advanced configurations, architecture logic, and debugging, please visit our Wiki:
* [System Architecture & Workflow](https://github.com/albis0103/NewsAbstract/wiki/System-Architecture-&-Documentation)
* [news-analyzer](https://github.com/albis0103/NewsAbstract/wiki/news%E2%80%90analyzer-Architecture-&-Documentation-(Python-Core-Engine))
* [news-dispatcher](https://github.com/albis0103/NewsAbstract/wiki/news%E2%80%90dispatcher-Architecture-and-Overview-(Java-Dispatch-Backend))
* [Troubleshooting & FAQ](https://github.com/albis0103/NewsAbstract/wiki/Troubleshooting-&-FAQ)
