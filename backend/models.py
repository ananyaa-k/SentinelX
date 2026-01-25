from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
import uuid

class YaraRule(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    rule_id: str
    name: str
    family: str = "Unknown"
    severity: str = "Medium"
    content: str
    source: str
    date_added: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ScanResult(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    filename: str
    filesize: int
    filetype: str
    status: str
    confidence: int
    detected_rules: List[str] = []
    ai_insight: str = ""
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class SyncRequest(BaseModel):
    sources: List[str] = ["github", "otx", "malwarebazaar"]
