# J.A.R.V.I.S - Autonomous AI Assistant

J.A.R.V.I.S is a highly advanced, multi-modal autonomous AI assistant built with a cyber-HUD interface. It is powered by Google's Gemini LLM and utilizes a LangGraph-based cognitive engine to plan, execute, and report on physical and digital tasks.

## 🧠 System Architecture

The project is split into two primary layers:

### 1. The Frontend (Cyber HUD)
A React + Vite web application built with a premium, dynamic cyber-aesthetic. It features real-time telemetry, a matrix-style background, and a dedicated execution log sidebar to monitor the AI's physical tool invocations.

### 2. The Backend (Cognitive Engine)
A Python FastAPI server that acts as the brain. The core orchestration happens in `app/agents/brain.py`, mapping incoming intents into JSON arrays.
- **Powered By**: Google Gemini API (`gemini-2.5-flash`)
- **Orchestration**: `langgraph` StateGraph workflow (Planner -> Executor -> Reporter)

## 🛠️ Built-In Capabilities (Tools)

J.A.R.V.I.S can perform actions locally on your machine via a mapped Tool Registry:
- **`system_browser`**: Physically launches applications or websites in your default browser.
- **`send_whatsapp`**: Uses Playwright automation to navigate WhatsApp Web and dispatch messages.
- **`send_email`**: Uses Playwright automation to draft and dispatch emails via Gmail.
- **`web_search`**: Leverages DuckDuckGo for real-time internet searches.
- **`web_scraper`**: Extracts and digests content from specific URLs.
- **`metadata_extractor`**: A digital forensics tool for extracting file metadata.

---

## 🚀 How to Start J.A.R.V.I.S

To bring the system online, you need to run **two separate terminal windows**.

### 1. Start the Backend API (Terminal 1)
Open a terminal, navigate to the `backend` folder, and launch Uvicorn:
```powershell
cd backend
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```
*(Ensure you have installed dependencies via `pip install -r backend/requirements.txt` and `python -m playwright install chromium`)*

### 2. Start the Frontend HUD (Terminal 2)
Open a **new** terminal, navigate to the `frontend` folder, and launch Vite:
```powershell
cd frontend
npm run dev
```

Once both are running, open your browser to the URL provided by Vite (usually `http://localhost:5173`) and you can begin interacting with J.A.R.V.I.S!

## 🔧 Automation Configuration

The WhatsApp and Gmail automation tools run via Playwright. By default, they are configured with `headless=False` so that you can scan the WhatsApp Web QR code and authenticate your Google account on the first run. The login state is saved inside persistent contexts in the `data/` directory so you won't need to log in twice.
