import asyncio
import requests
import logging
from typing import List, Dict, Any
from datetime import datetime, timedelta
import os

logger = logging.getLogger(__name__)

class ThreatFeedService:
    def __init__(self, otx_api_key: str, malwarebazaar_api: str, otx_base_url: str):
        self.otx_api_key = otx_api_key
        self.malwarebazaar_api = malwarebazaar_api
        self.otx_base_url = otx_base_url
        self.session = requests.Session()
    
    async def fetch_malwarebazaar_samples(self, limit: int = 100) -> Dict[str, Any]:
        """Fetch recent malware samples from MalwareBazaar"""
        try:
            response = self.session.post(
                self.malwarebazaar_api,
                data={"query": "get_recent", "selector": limit},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get("query_status") == "ok":
                    samples = data.get("data", [])
                    
                    processed_samples = []
                    for sample in samples[:20]:  # Limit to 20 for processing
                        processed_samples.append({
                            "sha256_hash": sample.get("sha256_hash"),
                            "file_type": sample.get("file_type"),
                            "file_name": sample.get("file_name"),
                            "signature": sample.get("signature"),
                            "tags": sample.get("tags", []),
                            "first_seen": sample.get("first_seen"),
                            "source": "malwarebazaar"
                        })
                    
                    logger.info(f"Fetched {len(processed_samples)} samples from MalwareBazaar")
                    return {
                        "status": "success",
                        "samples": processed_samples,
                        "total": len(processed_samples),
                        "timestamp": datetime.utcnow()
                    }
            
            return {
                "status": "failed",
                "samples": [],
                "total": 0,
                "error": f"HTTP {response.status_code}",
                "timestamp": datetime.utcnow()
            }
            
        except Exception as e:
            logger.error(f"MalwareBazaar fetch failed: {str(e)}")
            return {
                "status": "failed",
                "samples": [],
                "total": 0,
                "error": str(e),
                "timestamp": datetime.utcnow()
            }
    
    async def fetch_otx_pulses(self, limit: int = 50) -> Dict[str, Any]:
        """Fetch threat pulses from AlienVault OTX"""
        try:
            headers = {"X-OTX-API-KEY": self.otx_api_key}
            
            # Fetch subscribed pulses
            response = self.session.get(
                f"{self.otx_base_url}/pulses/subscribed",
                headers=headers,
                params={"limit": limit, "page": 1},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                pulses = data.get("results", [])
                
                processed_pulses = []
                for pulse in pulses[:20]:  # Limit to 20
                    indicators = []
                    for indicator in pulse.get("indicators", [])[:10]:  # Max 10 indicators per pulse
                        indicators.append({
                            "type": indicator.get("type"),
                            "indicator": indicator.get("indicator"),
                            "description": indicator.get("description", "")
                        })
                    
                    processed_pulses.append({
                        "id": pulse.get("id"),
                        "name": pulse.get("name"),
                        "description": pulse.get("description", ""),
                        "tags": pulse.get("tags", []),
                        "adversary": pulse.get("adversary", ""),
                        "targeted_countries": pulse.get("targeted_countries", []),
                        "malware_families": pulse.get("malware_families", []),
                        "attack_ids": pulse.get("attack_ids", []),
                        "indicators": indicators,
                        "created": pulse.get("created"),
                        "source": "otx"
                    })
                
                logger.info(f"Fetched {len(processed_pulses)} pulses from OTX")
                return {
                    "status": "success",
                    "pulses": processed_pulses,
                    "total": len(processed_pulses),
                    "timestamp": datetime.utcnow()
                }
            
            return {
                "status": "failed",
                "pulses": [],
                "total": 0,
                "error": f"HTTP {response.status_code}",
                "timestamp": datetime.utcnow()
            }
            
        except Exception as e:
            logger.error(f"OTX fetch failed: {str(e)}")
            return {
                "status": "failed",
                "pulses": [],
                "total": 0,
                "error": str(e),
                "timestamp": datetime.utcnow()
            }
    
    async def fetch_all_feeds(self) -> Dict[str, Any]:
        """Fetch from all threat intelligence sources"""
        results = {}
        
        # Fetch MalwareBazaar
        mb_result = await self.fetch_malwarebazaar_samples()
        results["malwarebazaar"] = mb_result
        
        # Small delay
        await asyncio.sleep(2)
        
        # Fetch OTX
        otx_result = await self.fetch_otx_pulses()
        results["otx"] = otx_result
        
        total_items = mb_result.get("total", 0) + otx_result.get("total", 0)
        
        return {
            "status": "success",
            "sources": results,
            "total_items": total_items,
            "timestamp": datetime.utcnow()
        }