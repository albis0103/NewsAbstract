
# SecOps News Analysis System

## 1. Environment Setup
Ensure that **Python 3.10+** and **Node.js** are installed. From the project root directory, run:

```powershell
# Install all necessary Python libraries
pip install -r requirements.txt
```
## 2. Launch Steps (By Operating System)
Windows (PowerShell)
PowerShell
```
# 1. Execute model initialization (Absolute path required)
python "[YOUR_PATH]\keyvector_model.py"
# 2. Set environment variables (Ensure n8n can access APIs)
$env:GEMINI_API_KEY="YOUR_GEMINI_KEY"
$env:JINA_API_KEY="YOUR_JINA_KEY"
$env:PYTHONIOENCODING="utf-8"
# 3. Start n8n
npx n8n
```
macOS / Linux (Terminal)
Bash
```
# 1. Execute model initialization (Absolute path)
python3 "/[YOUR_PATH]/keyvector_model.py"

# 2. Set environment variables
export GEMINI_API_KEY="YOUR_GEMINI_KEY"
export JINA_API_KEY="YOUR_JINA_KEY"
export PYTHONIOENCODING="utf-8"

# 3. Start n8n
npx n8n
```
## 3. n8n Workflow Initialization
Access n8n: Open your browser and navigate to http://localhost:5678.<br>
Import Workflow: Drag and drop my_workflow.json into the canvas.<br>
Official Deployment: Click Publish in the top-right corner (ensure the toggle turns green).<br>
## 4. Launch Frontend Tools
Locate Analyzer.html (分析器.html) in the project folder.<br>
Open it directly (Recommended: Save as a browser bookmark).<br>