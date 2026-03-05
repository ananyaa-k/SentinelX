# Sentinel-X Deployment Guide (Docker)

This guide provides instructions for deploying the Sentinel-X Next-Generation Malware Sandbox using Docker.

## Prerequisites
- **Docker** and **Docker Compose** installed on your host machine.
- Your **Google Gemini API Key**.
- (Optional) Your **AlienVault OTX API Key**.

## Step 1: Configuration

Before starting, ensure your API keys are passed to the environment. Create a `.env` file in the project directory (alongside `docker-compose.yml`) containing:

```env
GEMINI_API_KEY=your_gemini_api_key_here
OTX_API_KEY=your_otx_api_key_here
```

## Step 2: Build and Run

Run Docker Compose to build the multi-container application in detached mode.

```bash
docker-compose up --build -d
```

This will automatically pull necessary images and start three services:
1. `mongodb` - Persistent database for scans, YARA rules, and agent feedback.
2. `backend` - FastAPI server handling AI inference and YARA matching (Internal Port 8000).
3. `frontend` - React SPA served via Nginx (Available on Port 3000).

## Step 3: Verifying the Deployment

1. **Frontend Dashboard:** Open your web browser and navigate to `http://localhost:3000`. You should see the Sentinel-X dashboard.
2. **Backend API Docs:** Navigate to `http://localhost:8000/docs` to view and test the FastAPI Swagger UI.
3. **Container Health:** Run `docker ps` to verify all three containers are healthy.

## Real-Time Improvements & Agent Learning (Feedback Loop)
During this audit, the following enterprise-grade improvements were added:
1. **Server-Sent Events (SSE) Streaming:** The file scanning process now streams updates dynamically to the Command Center UI, eliminating blocking requests.
2. **Feedback API Endpoint:** Analysts can click "Mark False Positive" or "Confirm Threat" in the UI for analyzed files.
3. **Dynamic Prompt Injection:** The Gemini Service automatically fetches recent analyst feedback from MongoDB and injects it into its reasoning prompt. This enables localized agent learning without the need for manual fine-tuning, aggressively driving down false positives over time.

## Exposing to the Public
If you are hosting this on a cloud provider (AWS/GCP/DigitalOcean):
- Open ports `80` (or `3000`) and `8000` on your server's firewall.
- Inside `docker-compose.yml`, change `REACT_APP_BACKEND_URL=http://your-server-ip:8000` for the frontend build arguments to ensure client-side fetch requests reach the backend API successfully.
