import asyncio
import aiofiles
import requests
import logging
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime
import os

logger = logging.getLogger(__name__)

class GitHubYARASyncer:
    def __init__(self, base_url: str, rules_dir: str):
        self.base_url = base_url
        self.rules_dir = Path(rules_dir) / "github"
        self.rules_dir.mkdir(parents=True, exist_ok=True)
        
        # Known YARA rule files from ReversingLabs repo
        self.rule_files = [
            "ransomware.yar",
            "trojan.yar",
            "backdoor.yar",
            "banker.yar",
            "cryptominer.yar",
            "apt.yar",
            "exploit.yar",
            "webshell.yar"
        ]
    
    async def sync_rules(self) -> Dict[str, Any]:
        """Sync YARA rules from GitHub repository"""
        synced_rules = []
        errors = []
        
        try:
            for rule_file in self.rule_files:
                try:
                    url = f"{self.base_url}/{rule_file}"
                    response = requests.get(url, timeout=30)
                    
                    if response.status_code == 200:
                        rule_path = self.rules_dir / rule_file
                        async with aiofiles.open(rule_path, 'w') as f:
                            await f.write(response.text)
                        
                        synced_rules.append(rule_file)
                        logger.info(f"Synced rule: {rule_file}")
                    else:
                        error_msg = f"Failed to fetch {rule_file}: HTTP {response.status_code}"
                        errors.append(error_msg)
                        logger.warning(error_msg)
                    
                    # Be nice to GitHub
                    await asyncio.sleep(1)
                    
                except Exception as e:
                    error_msg = f"Error syncing {rule_file}: {str(e)}"
                    errors.append(error_msg)
                    logger.error(error_msg)
            
            return {
                "status": "success" if synced_rules else "failed",
                "synced_rules": synced_rules,
                "total_synced": len(synced_rules),
                "errors": errors,
                "timestamp": datetime.utcnow()
            }
            
        except Exception as e:
            logger.error(f"GitHub sync failed: {str(e)}")
            return {
                "status": "failed",
                "synced_rules": [],
                "total_synced": 0,
                "errors": [str(e)],
                "timestamp": datetime.utcnow()
            }
    
    async def get_rule_list(self) -> List[str]:
        """Get list of synced rules"""
        rules = []
        for rule_path in self.rules_dir.glob("*.yar"):
            rules.append(rule_path.name)
        return rules