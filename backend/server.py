from fastapi import FastAPI, APIRouter, UploadFile, File, BackgroundTasks, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from typing import List
from datetime import datetime, timezone
import uuid
import asyncio

# Import Services and Models
from services.yara_service import YaraService
from services.gemini_service import GeminiService
from services.feed_service import FeedService
from utils.scheduler import start_scheduler
from models import ScanResult, YaraRule, SyncRequest

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Configuration
MONGO_URL = os.environ['MONGO_URL']
DB_NAME = os.environ['DB_NAME']
YARA_RULES_DIR = os.environ.get("YARA_RULES_DIR", "/app/backend/yara_rules")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GITHUB_REPO = os.environ.get("GITHUB_YARA_REPO")
OTX_KEY = os.environ.get("OTX_API_KEY")

# Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize App and Database
app = FastAPI()
client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]

# Initialize Services
yara_service = YaraService(rules_dir=YARA_RULES_DIR)
gemini_service = GeminiService(api_key=GEMINI_API_KEY)
feed_service = FeedService(yara_repo_url=GITHUB_REPO, otx_key=OTX_KEY)

api_router = APIRouter(prefix="/api")

# --- Helper Functions ---

async def save_scan_result(result: ScanResult):
    """Saves scan result to MongoDB."""
    doc = result.model_dump()
    doc['timestamp'] = doc['timestamp'].isoformat()
    await db.scans.insert_one(doc)

async def sync_feeds_task(sources: List[str] = ["github", "otx", "malwarebazaar"]):
    """Background task to sync threat feeds."""
    logger.info(f"Starting feed sync for sources: {sources}")
    new_rules = await feed_service.fetch_all(sources)
    
    count = 0
    for rule_data in new_rules:
        # Check if rule exists by name
        existing = await db.rules.find_one({"name": rule_data["name"]})
        if not existing:
            # Save to DB
            rule = YaraRule(**rule_data)
            doc = rule.model_dump()
            doc['date_added'] = doc['date_added'].isoformat()
            await db.rules.insert_one(doc)
            
            # Save to Disk
            filename = f"{rule.rule_id}.yar"
            yara_service.save_rule(rule.content, filename)
            count += 1
            
    logger.info(f"Sync complete. Added {count} new rules.")

# --- Endpoints ---

@api_router.get("/")
async def root():
    return {"message": "SentinelX API Online"}

@api_router.post("/scan", response_model=ScanResult)
async def scan_file(file: UploadFile = File(...)):
    """
    Scans an uploaded file using YARA and Gemini AI.
    """
    try:
        content = await file.read()
        
        # 1. YARA Scan
        matches = yara_service.scan_data(content)
        
        status = "SAFE"
        confidence = 0
        ai_insight = "Clean file. No YARA matches found."
        
        if matches:
            status = "MALICIOUS"
            confidence = 100
            ai_insight = f"Detected by YARA rules: {', '.join(matches)}"
        else:
            # 2. AI Analysis (if no match)
            is_malicious, reason, ai_conf = await gemini_service.analyze_file(
                filename=file.filename,
                data=content,
                mime_type=file.content_type or "application/octet-stream"
            )
            
            if is_malicious:
                status = "MALICIOUS"
                confidence = ai_conf
                ai_insight = f"Gemini Insight: {reason}"
                
                # 3. Generate Rule (if malicious and not detected)
                rule_content = await gemini_service.generate_yara_rule(
                    filename=file.filename,
                    data=content,
                    reason=reason
                )
                
                if rule_content:
                    rule_name = f"auto_gen_{uuid.uuid4().hex[:8]}"
                    # Save rule
                    yara_service.save_rule(rule_content, f"{rule_name}.yar")
                    
                    # Persist Rule to DB
                    new_rule = YaraRule(
                        rule_id=rule_name,
                        name=f"Auto-Generated: {file.filename}",
                        family="AI-Detected",
                        severity="High",
                        content=rule_content,
                        source="Gemini-AI"
                    )
                    doc = new_rule.model_dump()
                    doc['date_added'] = doc['date_added'].isoformat()
                    await db.rules.insert_one(doc)
                    
                    ai_insight += " [New YARA Rule Generated]"
            else:
                status = "SAFE"
                confidence = ai_conf  # usually low for safe
                ai_insight = f"Gemini Insight (SAFE): {reason}"

        # Create Result
        result = ScanResult(
            filename=file.filename,
            filesize=len(content),
            filetype=file.content_type or "unknown",
            status=status,
            confidence=confidence,
            detected_rules=matches,
            ai_insight=ai_insight
        )
        
        # Save to DB
        await save_scan_result(result)
        
        return result

    except Exception as e:
        logger.error(f"Scan failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/rules", response_model=List[YaraRule])
async def get_rules():
    rules_cursor = db.rules.find({}, {"_id": 0}).sort("date_added", -1).limit(100)
    rules = await rules_cursor.to_list(length=100)
    
    # Date conversion
    for r in rules:
        if isinstance(r['date_added'], str):
            r['date_added'] = datetime.fromisoformat(r['date_added'])
            
    return rules

@api_router.post("/sync-rules")
async def trigger_sync_rules(request: SyncRequest, background_tasks: BackgroundTasks):
    background_tasks.add_task(sync_feeds_task, request.sources)
    return {"message": f"Rule sync started for {request.sources}"}

@api_router.get("/stats")
async def get_stats():
    """Returns dashboard stats."""
    total_scans = await db.scans.count_documents({})
    malicious = await db.scans.count_documents({"status": "MALICIOUS"})
    rules_count = await db.rules.count_documents({})
    
    return {
        "total_scans": total_scans,
        "malicious_detected": malicious,
        "active_rules": rules_count
    }

# Include Router
app.include_router(api_router)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    # Start Scheduler
    start_scheduler(sync_feeds_task, hours=24)
    logger.info("Application Startup Complete")

@app.on_event("shutdown")
async def shutdown_event():
    client.close()
