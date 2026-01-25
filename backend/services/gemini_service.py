from google import genai
import os
import logging
from typing import Tuple, Optional
import re

logger = logging.getLogger(__name__)

class GeminiService:
    def __init__(self, api_key: str):
        if not api_key:
            logger.warning("Gemini API Key is missing.")
            self.client = None
            return
            
        try:
            self.client = genai.Client(api_key=api_key)
            self.model_name = 'gemini-2.5-flash'
        except Exception as e:
            logger.error(f"Failed to initialize Gemini client: {e}")
            self.client = None

    def _extract_strings(self, data: bytes, min_length=4) -> str:
        """Extracts printable strings from binary data."""
        try:
            # Find ASCII strings
            words = re.findall(b"[ -~]{%d,}" % min_length, data)
            # Limit to first 2000 strings to fit context window
            return "\n".join([w.decode('utf-8', errors='ignore') for w in words[:2000]])
        except Exception:
            return ""

    async def analyze_file(self, filename: str, data: bytes, mime_type: str) -> Tuple[bool, str, int]:
        """
        Analyzes file metadata and strings to determine if malicious.
        Returns: (is_malicious, insight_text, confidence_score)
        """
        if not self.client:
            return False, "Gemini Analysis Unavailable (No Key)", 0

        strings_preview = self._extract_strings(data)
        
        prompt = f"""
        You are a malware analysis expert. Analyze the following file metadata and extracted strings.
        
        Filename: {filename}
        Type: {mime_type}
        Size: {len(data)} bytes
        
        Extracted Strings (preview):
        {strings_preview[:4000]} 
        
        Task:
        1. Determine if this file is likely MALICIOUS or SAFE.
        2. Provide a confidence score (0-100).
        3. Explain your reasoning in 2 sentences.
        
        Output Format:
        STATUS: [MALICIOUS/SAFE]
        CONFIDENCE: [0-100]
        REASON: [Your explanation]
        """

        try:
            # Note: The new SDK client is synchronous by default unless using async client.
            # But here we are in an async function.
            # For simplicity with google-genai 1.0+, we can use the sync call or look for async.
            # Most examples show sync calls. We can wrap it or just use it (it's fast enough for this MVP).
            # Or better, use `from google.genai import Client` which supports async via `aio`.
            # Let's check if the client has aio property or async methods. 
            # The output of web search didn't explicitly mention async.
            # I will use the standard sync call for now, as it's safer than guessing async method names.
            
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            
            text = response.text
            
            is_malicious = "STATUS: MALICIOUS" in text.upper()
            
            # Parse confidence
            confidence = 0
            conf_match = re.search(r"CONFIDENCE:\s*(\d+)", text, re.IGNORECASE)
            if conf_match:
                confidence = int(conf_match.group(1))
            
            # Parse reason
            reason = "No explanation provided."
            reason_match = re.search(r"REASON:\s*(.*)", text, re.IGNORECASE | re.DOTALL)
            if reason_match:
                reason = reason_match.group(1).strip()

            return is_malicious, reason, confidence

        except Exception as e:
            logger.error(f"Gemini analysis failed: {e}")
            return False, f"Analysis failed: {str(e)}", 0

    async def generate_yara_rule(self, filename: str, data: bytes, reason: str) -> Optional[str]:
        """Generates a YARA rule for a malicious file."""
        if not self.client:
            return None

        strings_preview = self._extract_strings(data)
        
        prompt = f"""
        Generate a valid YARA rule to detect this malicious file based on the analysis: "{reason}".
        
        Filename: {filename}
        Extracted Strings:
        {strings_preview[:3000]}
        
        Requirements:
        1. Rule name should be derived from filename or malware family.
        2. Use specific strings found in the preview.
        3. Include metadata (author="SentinelX AI", date).
        4. Output ONLY the raw YARA rule content, no markdown formatting.
        """

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            rule_content = response.text.strip()
            # Cleanup markdown code blocks if present
            rule_content = rule_content.replace("```yara", "").replace("```", "")
            return rule_content
        except Exception as e:
            logger.error(f"Gemini rule generation failed: {e}")
            return None
