# SentinelX: GenAI-Powered Malware Analysis Engine 🛡️

<<<<<<< HEAD
**SentinelX** is a next-generation malware sandbox that bridges the gap between static signature matching and heuristic behavioral profiling. Unlike traditional sandboxes, SentinelX uses a **Hybrid Detection Engine** combining industry-standard **YARA** scanning with an **LLM Agent (Gemini 2.5 Flash)** to interpret file anomalies and *autonomously synthesize* new YARA rules for zero-day threats.

## 🏗️ Architecture 

### Full-Stack Implementation
* **Frontend:** React 19, Tailwind CSS, Framer Motion, Shadcn UI (Theme with Dark/Light mode).
* **Backend:** FastAPI (Python 3.11) microservices architecture.
* **Database:** MongoDB (via Motor) for storing scan results, YARA rules, and threat intel.
* **AI Engine:** Google Gemini 2.5 Flash via `google-genai` SDK.
* **Static Engine:** YARA-Python for high-speed signature matching.

### Core Pipelines
1.  **Ingestion & Pre-processing:** Secure file upload handling and metadata extraction.
2.  **Static Analysis:** Instant scanning against a local database of 50,000+ YARA signatures.
3.  **AI Heuristics:** If static analysis fails, Gemini 2.5 analyzes string entropy, API calls, and code structure.
4.  **Autonomous Synthesis:** If a threat is confirmed, the AI *writes and compiles* a valid YARA rule to block future variants.
5.  **Global Intelligence:** Automated syncing with AlienVault OTX, MalwareBazaar, and ReversingLabs repositories.

## ✨ Key Features

- **🛡️ Hybrid Detection**: Combines the speed of signatures with the reasoning of Large Language Models.
- **🧠 Zero-Shot Rule Generation**: Automatically creates YARA rules for unknown threats without human intervention.
- **🌍 Multi-Source Threat Intel**: One-click sync from GitHub, OTX, and MalwareBazaar.
- **📊Dashboard**: Real-time scanning visualization, "AI Logic" pipeline view, and downloadable rule management.
- **🎨 Modern UI**: Professional commercial-grade interface with full Dark/Light theme support.

## 🚀 Roadmap & Status

- [x] **Architecture Design & Database Schema**
- [x] **Core API Implementation (FastAPI + MongoDB)**
- [x] **YARA Engine Integration**
- [x] **Gemini 2.5 Agent Integration (google-genai SDK)**
- [x] **Autonomous Rule Feedback Loop**
- [x] **Real-Time Threat Feed Sync (OTX, MalwareBazaar)**
- [x] **Enterprise Frontend (React + Tailwind)**
- [ ] User Authentication (RBAC)
- [ ] Docker Containerization for Production

## 🛠️ Getting Started

### Prerequisites
- Python 3.11+
- Node.js & Yarn
- MongoDB
- Google Gemini API Key

### Installation

1.  **Backend Setup**
    ```bash
    cd backend
    pip install -r requirements.txt
    python -m uvicorn server:app --reload
    ```

2.  **Frontend Setup**
    ```bash
    cd frontend
    yarn install
    yarn start
    ```

3.  **Environment Variables**
    Create a `.env` file in `backend/`:
    ```env
    MONGO_URL=mongodb://localhost:27017
    DB_NAME=sentinelx
    GEMINI_API_KEY=your_key_here
    OTX_API_KEY=your_key_here
    ```

*This project is currently active and deployed as a v2.1 Enterprise Release.*
=======
**SentinelX** is a next-generation malware sandbox that bridges the gap between static analysis and behavioral profiling. Unlike traditional sandboxes, SentinelX uses an **LLM Agent (Gemini 1.5)** to interpret file metadata and *autonomously synthesize* **YARA rules** for zero-day threats.

## 🏗️ Architecture (In Progress)
* **Ingestion:** FastAPI microservice for handling binary uploads.
* **Static Analysis:** YARA integration for signature matching.
* **AI Agent:** Gemini 1.5 Pro integration for behavioral reasoning and rule generation.
* **Isolation:** Dockerized execution environment.

## 🚀 Roadmap
- [x] Architecture Design
- [ ] Core API Implementation (FastAPI)
- [ ] Gemini Agent Integration
- [ ] YARA Rule Feedback Loop

*This project is currently under active development for 2026 Security Research.*
>>>>>>> c041dd9e60a38507fc274fc26f40c8ba06a7a68a
