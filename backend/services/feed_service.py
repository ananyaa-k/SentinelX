import aiohttp
import logging
from typing import List, Dict
import os
import re

logger = logging.getLogger(__name__)

class FeedService:
    def __init__(self, yara_repo_url: str, otx_key: str):
        self.yara_repo_url = yara_repo_url
        self.otx_key = otx_key
        # GitHub Raw URLs for YARA rules
        self.github_urls = [
            "https://raw.githubusercontent.com/Yara-Rules/rules/master/malware/MALW_Eicar.yar",
            "https://raw.githubusercontent.com/Yara-Rules/rules/master/malware/MALW_Mimispoofer.yar",
            "https://raw.githubusercontent.com/ReversingLabs/reversinglabs-yara-rules/develop/yara/trojan/Win32.Trojan.Zeus.yar"
        ]

    async def fetch_all(self, sources: List[str]) -> List[Dict[str, str]]:
        """Orchestrates fetching from multiple sources."""
        all_rules = []
        
        if "github" in sources:
            all_rules.extend(await self.fetch_github_rules())
            
        if "otx" in sources:
            all_rules.extend(await self.fetch_otx_rules())
            
        if "malwarebazaar" in sources:
            all_rules.extend(await self.fetch_malwarebazaar_rules())
            
        return all_rules

    async def fetch_github_rules(self) -> List[Dict[str, str]]:
        """Fetches raw YARA rules from GitHub."""
        logger.info("Fetching rules from GitHub...")
        new_rules = []
        async with aiohttp.ClientSession() as session:
            for url in self.github_urls:
                try:
                    async with session.get(url) as response:
                        if response.status == 200:
                            content = await response.text()
                            filename = url.split('/')[-1]
                            # Simple parsing to get rule name
                            name_match = re.search(r'rule\s+(\w+)', content)
                            rule_name = name_match.group(1) if name_match else filename.replace('.', '_')
                            
                            new_rules.append({
                                "rule_id": rule_name,
                                "name": rule_name,
                                "content": content,
                                "source": "GitHub-Community",
                                "family": "General",
                                "severity": "High"
                            })
                except Exception as e:
                    logger.error(f"Failed to fetch GitHub rule {url}: {e}")
        return new_rules

    async def fetch_otx_rules(self) -> List[Dict[str, str]]:
        """Fetches pulses from OTX and converts IOCs to YARA rules."""
        if not self.otx_key:
            return []
        
        logger.info("Fetching pulses from OTX...")
        new_rules = []
        url = "https://otx.alienvault.com/api/v1/pulses/subscribed"
        headers = {"X-OTX-API-KEY": self.otx_key}
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        for pulse in data.get('results', [])[:5]: # Limit to 5 for demo
                            pulse_name = pulse.get('name', 'Unknown Pulse')
                            pulse_id = pulse.get('id', '')
                            
                            # Create a simple metadata rule
                            content = f"""
rule OTX_{pulse_id} {{
    meta:
        description = "OTX Pulse: {pulse_name}"
        author = "SentinelX OTX Sync"
        date = "{pulse.get('modified', '')}"
    condition:
        false
}}"""
                            new_rules.append({
                                "rule_id": f"OTX_{pulse_id}",
                                "name": pulse_name,
                                "content": content,
                                "source": "AlienVault-OTX",
                                "family": "Threat-Pulse",
                                "severity": "Medium"
                            })
        except Exception as e:
            logger.error(f"OTX fetch failed: {e}")
            
        return new_rules

    async def fetch_malwarebazaar_rules(self) -> List[Dict[str, str]]:
        """Fetches recent malware hashes from MalwareBazaar and creates hash-based rules."""
        logger.info("Fetching recent threats from MalwareBazaar...")
        new_rules = []
        url = "https://mb-api.abuse.ch/api/v1/"
        
        try:
            async with aiohttp.ClientSession() as session:
                # Query for recent generic malware tags
                payload = {'query': 'get_recent', 'selector': 'time'}
                async with session.post(url, data=payload) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get('query_status') == 'ok':
                            # Create a single rule for recent hashes (batch of 50)
                            samples = data.get('data', [])[:20]
                            hashes = [s.get('sha256_hash') for s in samples if s.get('sha256_hash')]
                            
                            if hashes:
                                rule_name = f"MalwareBazaar_Recent_{len(hashes)}"
                                hash_conditions = "\n        ".join([f'hash.sha256(0, filesize) == "{h}" or' for h in hashes])
                                hash_conditions = hash_conditions.rstrip(" or")
                                
                                content = f"""
import "hash"

rule {rule_name} {{
    meta:
        description = "Detects recent malware hashes from MalwareBazaar"
        author = "SentinelX Feed"
        source = "MalwareBazaar"
    condition:
        {hash_conditions}
}}"""
                                new_rules.append({
                                    "rule_id": rule_name,
                                    "name": "MalwareBazaar Recent Hashes",
                                    "content": content,
                                    "source": "MalwareBazaar",
                                    "family": "Various",
                                    "severity": "Critical"
                                })
        except Exception as e:
            logger.error(f"MalwareBazaar fetch failed: {e}")
            
        return new_rules
