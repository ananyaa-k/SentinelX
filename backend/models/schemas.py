from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class ThreatSource(str, Enum):
    GITHUB = "github"
    MALWAREBAZAAR = "malwarebazaar"
    OTX = "otx"
    MANUAL = "manual"

class ScanStatus(str, Enum):
    SAFE = "SAFE"
    MALICIOUS = "MALICIOUS"
    SUSPICIOUS = "SUSPICIOUS"
    ERROR = "ERROR"

class YARARule(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str
    name: str
    content: str
    source: ThreatSource
    tags: List[str] = []
    description: Optional[str] = None
    confidence: float = 0.0
    validated: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class ThreatFeed(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str
    source: ThreatSource
    threat_type: str
    indicators: List[str]
    description: str
    severity: str
    metadata: Dict[str, Any] = {}
    fetched_at: datetime = Field(default_factory=datetime.utcnow)

class FileUploadResponse(BaseModel):
    filename: str
    file_size: int
    scan_status: ScanStatus
    confidence: float
    matched_rules: List[Dict[str, Any]]
    detected_strings: List[str]
    ai_analysis: Optional[str] = None
    scan_time: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class GenerateRuleRequest(BaseModel):
    threat_data: Dict[str, Any]
    threat_type: str
    severity: str
    description: str

class GenerateRuleResponse(BaseModel):
    rule_name: str
    rule_content: str
    confidence: float
    validated: bool
    validation_errors: List[str] = []
    ai_reasoning: str

class SyncStatus(BaseModel):
    source: str
    status: str
    rules_synced: int
    last_sync: datetime
    errors: List[str] = []

class ThreatIntelStats(BaseModel):
    total_rules: int
    github_rules: int
    generated_rules: int
    validated_rules: int
    last_github_sync: Optional[datetime] = None
    last_feed_fetch: Optional[datetime] = None