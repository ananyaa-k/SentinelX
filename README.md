# SentinelX: GenAI-Powered Malware Analysis Engine 🛡️

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
