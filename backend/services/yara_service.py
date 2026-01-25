import yara
import os
import glob
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class YaraService:
    def __init__(self, rules_dir: str):
        self.rules_dir = rules_dir
        self.rules = None
        self._ensure_rules_dir()
        self.compile_rules()

    def _ensure_rules_dir(self):
        os.makedirs(self.rules_dir, exist_ok=True)

    def compile_rules(self):
        """Compiles all YARA rules in the rules directory."""
        filepaths = glob.glob(os.path.join(self.rules_dir, "*.yar"))
        filepaths += glob.glob(os.path.join(self.rules_dir, "*.yara"))
        
        if not filepaths:
            logger.warning("No YARA rules found to compile.")
            self.rules = None
            return

        yara_files = {os.path.splitext(os.path.basename(f))[0]: f for f in filepaths}
        
        try:
            self.rules = yara.compile(filepaths=yara_files)
            logger.info(f"Successfully compiled {len(yara_files)} rule files.")
        except yara.SyntaxError as e:
            logger.error(f"YARA compilation error: {e}")
            # Try to compile valid ones one by one to avoid total failure? 
            # For now, just log and skip.
            self.rules = None
        except Exception as e:
            logger.error(f"Unexpected error compiling rules: {e}")
            self.rules = None

    def scan_data(self, data: bytes) -> List[str]:
        """Scans bytes and returns a list of matched rule names."""
        if not self.rules:
            # Try re-compiling if rules are missing (maybe added recently)
            self.compile_rules()
            if not self.rules:
                return []

        try:
            matches = self.rules.match(data=data)
            return [match.rule for match in matches]
        except Exception as e:
            logger.error(f"Error during YARA scan: {e}")
            return []

    def save_rule(self, rule_content: str, filename: str) -> bool:
        """Saves a new YARA rule to disk and recompiles."""
        try:
            path = os.path.join(self.rules_dir, filename)
            with open(path, 'w') as f:
                f.write(rule_content)
            self.compile_rules()
            return True
        except Exception as e:
            logger.error(f"Failed to save rule {filename}: {e}")
            return False
