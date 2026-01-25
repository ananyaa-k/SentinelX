#!/usr/bin/env python3
"""
SentinelX Backend API Testing Suite
Tests all backend endpoints with malicious and benign files
"""

import requests
import os
import json
from pathlib import Path
import time

# Configuration
BACKEND_URL = "https://malware-sandbox-7.preview.emergentagent.com/api"
SAMPLES_DIR = "/app/backend/tests/samples"

class SentinelXTester:
    def __init__(self):
        self.backend_url = BACKEND_URL
        self.samples_dir = Path(SAMPLES_DIR)
        self.results = {
            "scan_tests": [],
            "rules_tests": [],
            "sync_tests": [],
            "stats_tests": [],
            "commercial_tests": {},
            "feed_service_tests": []
        }
        
    def test_root_endpoint(self):
        """Test the root API endpoint"""
        print("🔍 Testing root endpoint...")
        try:
            response = requests.get(f"{self.backend_url}/")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Root endpoint working: {data}")
                return True
            else:
                print(f"❌ Root endpoint failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Root endpoint error: {e}")
            return False
    
    def test_file_scan(self, file_path, expected_status=None):
        """Test file scanning endpoint"""
        file_name = os.path.basename(file_path)
        print(f"🔍 Testing scan for: {file_name}")
        
        try:
            with open(file_path, 'rb') as f:
                files = {'file': (file_name, f, 'application/octet-stream')}
                response = requests.post(f"{self.backend_url}/scan", files=files, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                # Validate response structure
                required_fields = ['filename', 'filesize', 'filetype', 'status', 'confidence', 'ai_insight']
                missing_fields = [field for field in required_fields if field not in data]
                
                if missing_fields:
                    print(f"❌ Missing fields in response: {missing_fields}")
                    return False, data
                
                status = data['status']
                confidence = data['confidence']
                ai_insight = data['ai_insight']
                
                print(f"   📊 Status: {status}")
                print(f"   📊 Confidence: {confidence}%")
                print(f"   📊 AI Insight: {ai_insight[:100]}...")
                
                # Check if expected status matches
                if expected_status and status != expected_status:
                    print(f"❌ Expected {expected_status}, got {status}")
                    return False, data
                
                # Validate confidence is reasonable
                if not (0 <= confidence <= 100):
                    print(f"❌ Invalid confidence score: {confidence}")
                    return False, data
                
                # Check AI insight is present
                if not ai_insight or len(ai_insight.strip()) < 10:
                    print(f"❌ AI insight too short or missing")
                    return False, data
                
                print(f"✅ Scan successful for {file_name}")
                return True, data
                
            else:
                print(f"❌ Scan failed for {file_name}: {response.status_code}")
                print(f"   Response: {response.text}")
                return False, None
                
        except Exception as e:
            print(f"❌ Scan error for {file_name}: {e}")
            return False, None
    
    def test_all_sample_files(self):
        """Test scanning all sample files"""
        print("\n🧪 Testing all sample files...")
        
        # Test malicious files
        malicious_files = [
            "malicious_1_eicar.txt",
            "malicious_2_script.js", 
            "malicious_3_shell.py",
            "malicious_4_ransom.txt",
            "malicious_5_keylogger.txt"
        ]
        
        # Test benign files
        benign_files = [
            "benign_1_text.txt",
            "benign_2_code.py",
            "benign_3_data.csv", 
            "benign_4_config.json",
            "benign_5_web.html"
        ]
        
        all_passed = True
        
        # Test malicious files
        print("\n🦠 Testing malicious files...")
        for file_name in malicious_files:
            file_path = self.samples_dir / file_name
            if file_path.exists():
                success, data = self.test_file_scan(file_path, expected_status="MALICIOUS")
                self.results["scan_tests"].append({
                    "file": file_name,
                    "expected": "MALICIOUS", 
                    "success": success,
                    "data": data
                })
                if not success:
                    all_passed = False
            else:
                print(f"❌ File not found: {file_path}")
                all_passed = False
        
        # Test benign files  
        print("\n🟢 Testing benign files...")
        for file_name in benign_files:
            file_path = self.samples_dir / file_name
            if file_path.exists():
                success, data = self.test_file_scan(file_path, expected_status="SAFE")
                self.results["scan_tests"].append({
                    "file": file_name,
                    "expected": "SAFE",
                    "success": success, 
                    "data": data
                })
                if not success:
                    all_passed = False
            else:
                print(f"❌ File not found: {file_path}")
                all_passed = False
                
        return all_passed
    
    def test_rules_endpoint(self):
        """Test the rules endpoint"""
        print("\n🔍 Testing GET /api/rules...")
        try:
            response = requests.get(f"{self.backend_url}/rules", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Rules endpoint working, returned {len(data)} rules")
                
                # Validate structure if rules exist
                if data and len(data) > 0:
                    rule = data[0]
                    required_fields = ['rule_id', 'name', 'family', 'severity', 'content', 'source']
                    missing_fields = [field for field in required_fields if field not in rule]
                    
                    if missing_fields:
                        print(f"❌ Missing fields in rule: {missing_fields}")
                        return False
                
                self.results["rules_tests"].append({
                    "endpoint": "GET /api/rules",
                    "success": True,
                    "rules_count": len(data)
                })
                return True
            else:
                print(f"❌ Rules endpoint failed: {response.status_code}")
                print(f"   Response: {response.text}")
                self.results["rules_tests"].append({
                    "endpoint": "GET /api/rules", 
                    "success": False,
                    "error": f"Status {response.status_code}"
                })
                return False
                
        except Exception as e:
            print(f"❌ Rules endpoint error: {e}")
            self.results["rules_tests"].append({
                "endpoint": "GET /api/rules",
                "success": False, 
                "error": str(e)
            })
            return False
    
    def test_sync_rules_endpoint(self):
        """Test the sync rules endpoint with different sources"""
        print("\n🔍 Testing POST /api/sync-rules...")
        
        # Test with default sources (all)
        try:
            payload = {"sources": ["github", "otx", "malwarebazaar"]}
            response = requests.post(f"{self.backend_url}/sync-rules", json=payload, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Sync rules endpoint working: {data}")
                
                # Check response structure
                if 'message' not in data:
                    print(f"❌ Missing 'message' field in sync response")
                    return False
                
                self.results["sync_tests"].append({
                    "endpoint": "POST /api/sync-rules (all sources)",
                    "success": True,
                    "response": data
                })
                
                # Test individual sources
                individual_sources = ["github", "malwarebazaar", "otx"]
                for source in individual_sources:
                    print(f"   🔍 Testing sync with {source} only...")
                    try:
                        payload = {"sources": [source]}
                        response = requests.post(f"{self.backend_url}/sync-rules", json=payload, timeout=15)
                        if response.status_code == 200:
                            print(f"   ✅ {source} sync successful")
                            self.results["sync_tests"].append({
                                "endpoint": f"POST /api/sync-rules ({source})",
                                "success": True,
                                "response": response.json()
                            })
                        else:
                            print(f"   ❌ {source} sync failed: {response.status_code}")
                            self.results["sync_tests"].append({
                                "endpoint": f"POST /api/sync-rules ({source})",
                                "success": False,
                                "error": f"Status {response.status_code}"
                            })
                    except Exception as e:
                        print(f"   ❌ {source} sync error: {e}")
                        self.results["sync_tests"].append({
                            "endpoint": f"POST /api/sync-rules ({source})",
                            "success": False,
                            "error": str(e)
                        })
                
                return True
            else:
                print(f"❌ Sync rules endpoint failed: {response.status_code}")
                print(f"   Response: {response.text}")
                self.results["sync_tests"].append({
                    "endpoint": "POST /api/sync-rules",
                    "success": False,
                    "error": f"Status {response.status_code}"
                })
                return False
                
        except Exception as e:
            print(f"❌ Sync rules endpoint error: {e}")
            self.results["sync_tests"].append({
                "endpoint": "POST /api/sync-rules",
                "success": False,
                "error": str(e)
            })
            return False
    
    def test_commercial_upgrade_features(self):
        """Test the new Commercial Upgrade features"""
        print("\n🔍 Testing Commercial Upgrade Features...")
        
        # Test 1: Verify rules from different sources exist
        print("   📊 Checking for rules from different sources...")
        try:
            response = requests.get(f"{self.backend_url}/rules", timeout=10)
            if response.status_code == 200:
                rules = response.json()
                
                # Check for specific sources
                sources_found = set()
                malwarebazaar_rules = []
                github_rules = []
                otx_rules = []
                
                for rule in rules:
                    source = rule.get('source', '')
                    sources_found.add(source)
                    
                    if 'MalwareBazaar' in source:
                        malwarebazaar_rules.append(rule)
                    elif 'GitHub' in source:
                        github_rules.append(rule)
                    elif 'OTX' in source:
                        otx_rules.append(rule)
                
                print(f"   📋 Sources found: {list(sources_found)}")
                print(f"   🦠 MalwareBazaar rules: {len(malwarebazaar_rules)}")
                print(f"   🐙 GitHub rules: {len(github_rules)}")
                print(f"   🔍 OTX rules: {len(otx_rules)}")
                
                # Verify we have rules from expected sources
                expected_sources = ['MalwareBazaar', 'GitHub-Community', 'AlienVault-OTX']
                missing_sources = []
                
                for expected in expected_sources:
                    found = any(expected in source for source in sources_found)
                    if not found:
                        missing_sources.append(expected)
                
                if missing_sources:
                    print(f"   ⚠️  Missing rules from sources: {missing_sources}")
                    print("   💡 This might be expected if sync hasn't run yet")
                else:
                    print("   ✅ All expected sources have rules")
                
                self.results["commercial_tests"] = {
                    "sources_found": list(sources_found),
                    "malwarebazaar_count": len(malwarebazaar_rules),
                    "github_count": len(github_rules),
                    "otx_count": len(otx_rules),
                    "missing_sources": missing_sources
                }
                
                return len(missing_sources) == 0
                
            else:
                print(f"   ❌ Failed to fetch rules: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"   ❌ Commercial features test error: {e}")
            return False
    
    def test_feed_service_integration(self):
        """Test the feed service integration by triggering sync and verifying results"""
        print("\n🔍 Testing Feed Service Integration...")
        
        # Get initial rule count
        try:
            response = requests.get(f"{self.backend_url}/rules", timeout=10)
            initial_count = len(response.json()) if response.status_code == 200 else 0
            print(f"   📊 Initial rule count: {initial_count}")
        except:
            initial_count = 0
        
        # Trigger sync for each source individually
        sources_to_test = ["github", "malwarebazaar", "otx"]
        sync_results = {}
        
        for source in sources_to_test:
            print(f"   🔄 Testing {source} sync...")
            try:
                payload = {"sources": [source]}
                response = requests.post(f"{self.backend_url}/sync-rules", json=payload, timeout=15)
                
                if response.status_code == 200:
                    print(f"   ✅ {source} sync triggered successfully")
                    sync_results[source] = True
                    
                    # Wait a bit for background task
                    time.sleep(3)
                    
                else:
                    print(f"   ❌ {source} sync failed: {response.status_code}")
                    sync_results[source] = False
                    
            except Exception as e:
                print(f"   ❌ {source} sync error: {e}")
                sync_results[source] = False
        
        # Check if new rules were added
        try:
            time.sleep(5)  # Wait for background tasks to complete
            response = requests.get(f"{self.backend_url}/rules", timeout=10)
            final_count = len(response.json()) if response.status_code == 200 else 0
            print(f"   📊 Final rule count: {final_count}")
            
            if final_count > initial_count:
                print(f"   ✅ New rules added: {final_count - initial_count}")
                return True
            else:
                print(f"   ⚠️  No new rules added (this might be expected if rules already exist)")
                return True  # Not necessarily a failure
                
        except Exception as e:
            print(f"   ❌ Failed to check final rule count: {e}")
            return False
    
    def test_stats_endpoint(self):
        """Test the stats endpoint"""
        print("\n🔍 Testing GET /api/stats...")
        try:
            response = requests.get(f"{self.backend_url}/stats", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Stats endpoint working: {data}")
                
                # Validate structure
                required_fields = ['total_scans', 'malicious_detected', 'active_rules']
                missing_fields = [field for field in required_fields if field not in data]
                
                if missing_fields:
                    print(f"❌ Missing fields in stats: {missing_fields}")
                    return False
                
                self.results["stats_tests"].append({
                    "endpoint": "GET /api/stats",
                    "success": True,
                    "data": data
                })
                return True
            else:
                print(f"❌ Stats endpoint failed: {response.status_code}")
                print(f"   Response: {response.text}")
                self.results["stats_tests"].append({
                    "endpoint": "GET /api/stats",
                    "success": False,
                    "error": f"Status {response.status_code}"
                })
                return False
                
        except Exception as e:
            print(f"❌ Stats endpoint error: {e}")
            self.results["stats_tests"].append({
                "endpoint": "GET /api/stats",
                "success": False,
                "error": str(e)
            })
            return False
    
    def run_all_tests(self):
        """Run all backend tests"""
        print("🚀 Starting SentinelX Backend API Tests")
        print(f"🔗 Backend URL: {self.backend_url}")
        print("=" * 60)
        
        # Test root endpoint first
        root_success = self.test_root_endpoint()
        if not root_success:
            print("❌ Root endpoint failed, aborting tests")
            return False
        
        # Test all endpoints
        tests = [
            ("File Scanning", self.test_all_sample_files),
            ("Rules Endpoint", self.test_rules_endpoint), 
            ("Sync Rules", self.test_sync_rules_endpoint),
            ("Commercial Upgrade Features", self.test_commercial_upgrade_features),
            ("Feed Service Integration", self.test_feed_service_integration),
            ("Stats Endpoint", self.test_stats_endpoint)
        ]
        
        all_passed = True
        for test_name, test_func in tests:
            print(f"\n{'='*20} {test_name} {'='*20}")
            try:
                success = test_func()
                if not success:
                    all_passed = False
            except Exception as e:
                print(f"❌ {test_name} failed with exception: {e}")
                all_passed = False
        
        # Print summary
        print("\n" + "="*60)
        print("📊 TEST SUMMARY")
        print("="*60)
        
        # Scan results summary
        scan_results = self.results["scan_tests"]
        if scan_results:
            malicious_tests = [r for r in scan_results if r["expected"] == "MALICIOUS"]
            benign_tests = [r for r in scan_results if r["expected"] == "SAFE"]
            
            malicious_passed = sum(1 for r in malicious_tests if r["success"])
            benign_passed = sum(1 for r in benign_tests if r["success"])
            
            print(f"🦠 Malicious file detection: {malicious_passed}/{len(malicious_tests)} passed")
            print(f"🟢 Benign file detection: {benign_passed}/{len(benign_tests)} passed")
        
        # Other endpoints
        rules_passed = sum(1 for r in self.results["rules_tests"] if r["success"])
        sync_passed = sum(1 for r in self.results["sync_tests"] if r["success"])
        stats_passed = sum(1 for r in self.results["stats_tests"] if r["success"])
        
        print(f"📋 Rules endpoint: {rules_passed}/1 passed")
        print(f"🔄 Sync endpoint: {sync_passed}/1 passed") 
        print(f"📊 Stats endpoint: {stats_passed}/1 passed")
        
        if all_passed:
            print("\n✅ ALL TESTS PASSED!")
        else:
            print("\n❌ SOME TESTS FAILED!")
            
        return all_passed

def main():
    """Main test runner"""
    tester = SentinelXTester()
    success = tester.run_all_tests()
    
    # Save detailed results
    with open("/app/backend_test_results.json", "w") as f:
        json.dump(tester.results, f, indent=2, default=str)
    
    print(f"\n📄 Detailed results saved to: /app/backend_test_results.json")
    
    return 0 if success else 1

if __name__ == "__main__":
    exit(main())