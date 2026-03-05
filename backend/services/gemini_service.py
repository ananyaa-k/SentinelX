from google import genai
import os
import logging
from typing import Tuple, Optional
import re
import asyncio

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

    async def analyze_file(self, filename: str, data: bytes, mime_type: str, feedback_context: list = None) -> Tuple[bool, str, int]:
        """
        Analyzes file metadata and strings to determine if malicious.
        Returns: (is_malicious, insight_text, confidence_score)
        """
        if not self.client:
            return False, "Gemini Analysis Unavailable (No Key)", 0

        strings_preview = self._extract_strings(data)
        
        feedback_str = ""
        if feedback_context:
            feedback_str = "\nLearnings from previous Analyst Feedback (CRITICAL - DO NOT REPEAT FALSE POSITIVES):\n"
            for fb in feedback_context:
                feedback_str += f"- File '{fb.get('filename','unknown')}': Analyst marked as {fb.get('analyst_decision')}."
                if fb.get('notes'):
                    feedback_str += f" Notes: {fb.get('notes')}"
                feedback_str += "\n"

        prompt = f"""
        You are an expert malware reverse-engineer. Analyze the provided file metadata and extracted strings.
        {feedback_str}
        
        Filename: {filename}
        Type: {mime_type}
        Size: {len(data)} bytes
        
        Extracted Strings (preview):
        {strings_preview[:4000]} 
        
        Task:
        1. First, reason step-by-step about the file based on the extracted strings and metadata. Are there obvious malicious indicators?
        2. Be extremely careful to avoid false positives. If the strings look like a standard library, plain text file, or benign application without explicit malicious intent, you MUST classify it as SAFE.
        3. After reasoning, determine the final status (MALICIOUS or SAFE) and provide a confidence score (0-100).
        
        Strict Output Format (Follow exactly):
        REASON: [Write your step-by-step analysis here]
        STATUS: [MALICIOUS or SAFE]
        CONFIDENCE: [0-100]
        """

        try:
            # Use asyncio.to_thread to prevent blocking the async event loop, set temperature 0 to make it deterministic
            response = await asyncio.to_thread(
                self.client.models.generate_content,
                model=self.model_name,
                contents=prompt,
                config={"temperature": 0.0}
            )
            
            text = response.text
            
            # Parse reason first
            reason = "No explanation provided."
            reason_match = re.search(r"REASON:\s*(.*?)(?=\nSTATUS:|\nCONFIDENCE:|$)", text, re.IGNORECASE | re.DOTALL)
            if reason_match:
                reason = reason_match.group(1).strip()

            is_malicious = "STATUS: MALICIOUS" in text.upper()
            
            # Parse confidence
            confidence = 0
            conf_match = re.search(r"CONFIDENCE:\s*(\d+)", text, re.IGNORECASE)
            if conf_match:
                confidence = int(conf_match.group(1))

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
            response = await asyncio.to_thread(
                self.client.models.generate_content,
                model=self.model_name,
                contents=prompt,
                config={"temperature": 0.1}
            )
            rule_content = response.text.strip()
            # Cleanup markdown code blocks if present
            rule_content = rule_content.replace("```yara", "").replace("```", "")
            return rule_content
        except Exception as e:
            logger.error(f"Gemini rule generation failed: {e}")
            return None
