
#!/usr/bin/env python3
"""
Prompt Update Automation - UniMarketplace Assistant

This script automates the prompt update workflow including:
- Version control integration
- Automated testing pipeline
- Deployment with rollback capabilities
- Change approval tracking

Note: This is a conceptual implementation for assessment purposes.
Production version would include full error handling, logging,
and API integrations.

Usage:
    python automation-concept.py --change-type safety --version 1.1.1 --description "Fix escalation trigger"
    python automation-concept.py --deploy --version 1.1.0 --environment staging
    python automation-concept.py --rollback --target v1.0.9 --reason "Test failure"
"""

import json
import subprocess
import hashlib
import os
import sys
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Tuple
import argparse

# =============================================================================
# Configuration
# =============================================================================

class Environment(Enum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"

class ChangeType(Enum):
    TYPO = "typo"
    NAVIGATION = "navigation"
    TRANSACTION = "transaction"
    SAFETY = "safety"
    POLICY = "policy"
    ESCALATION = "escalation"

class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

# Approval matrix: which roles must approve each change type
APPROVAL_MATRIX = {
    ChangeType.TYPO: ["engineering"],
    ChangeType.NAVIGATION: ["engineering"],
    ChangeType.TRANSACTION: ["engineering", "policy"],
    ChangeType.SAFETY: ["engineering", "policy", "security"],
    ChangeType.POLICY: ["engineering", "policy", "security", "academic_office"],
    ChangeType.ESCALATION: ["engineering", "policy", "security"],
}

# Pass rate thresholds for deployment
PASS_RATE_THRESHOLDS = {
    "overall": 0.95,
    "safety": 1.0,
    "escalation": 1.0,
}

# Risk level by change type
RISK_LEVELS = {
    ChangeType.TYPO: RiskLevel.LOW,
    ChangeType.NAVIGATION: RiskLevel.LOW,
    ChangeType.TRANSACTION: RiskLevel.MEDIUM,
    ChangeType.SAFETY: RiskLevel.HIGH,
    ChangeType.POLICY: RiskLevel.HIGH,
    ChangeType.ESCALATION: RiskLevel.HIGH,
}

# =============================================================================
# Version Control Integration
# =============================================================================

class VersionControl:
    """Handles git operations for prompt versioning"""
    
    def __init__(self, repo_path: str = "."):
        self.repo_path = repo_path
    
    def create_branch(self, branch_name: str, change_type: ChangeType) -> str:
        """Create feature branch with naming convention"""
        branch = f"feature/{change_type.value}/{branch_name}"
        print(f"Creating branch: {branch}")
        subprocess.run(["git", "checkout", "-b", branch], cwd=self.repo_path, check=True)
        return branch
    
    def commit_changes(self, message: str, change_type: ChangeType, category: str) -> str:
        """Commit with standardized message format"""
        commit_msg = f"[{change_type.value.upper()}][{category.upper()}] {message}"
        print(f"Committing: {commit_msg}")
        subprocess.run(["git", "add", "prompt.md"], cwd=self.repo_path, check=True)
        subprocess.run(["git", "commit", "-m", commit_msg], cwd=self.repo_path, check=True)
        return self.get_current_commit_hash()
    
    def get_current_commit_hash(self) -> str:
        """Get current git commit hash"""
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            cwd=self.repo_path,
            check=True
        )
        return result.stdout.strip()
    
    def tag_version(self, version: str) -> bool:
        """Create version tag for deployment"""
        try:
            print(f"Creating tag: v{version}")
            subprocess.run(["git", "tag", f"v{version}"], cwd=self.repo_path, check=True)
            subprocess.run(["git", "push", "origin", f"v{version}"], cwd=self.repo_path, check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Tagging failed: {e}")
            return False
    
    def rollback_to_version(self, version: str) -> bool:
        """Rollback to previous version tag"""
        try:
            print(f"⏮Rolling back to v{version}")
            subprocess.run(["git", "checkout", f"v{version}"], cwd=self.repo_path, check=True)
            print(f"Successfully rolled back to v{version}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Rollback failed: {e}")
            return False
    
    def get_previous_version(self, current: str) -> Optional[str]:
        """Get previous version from git tags"""
        try:
            result = subprocess.run(
                ["git", "describe", "--tags", "--abbrev=0", f"v{current}^"],
                capture_output=True,
                text=True,
                cwd=self.repo_path
            )
            if result.returncode == 0:
                return result.stdout.strip().replace("v", "")
            return None
        except Exception:
            return None


# =============================================================================
# Automated Testing Pipeline
# =============================================================================

class TestRunner:
    """Executes golden tests and validates pass rates"""
    
    def __init__(self, test_cases_path: str = "test-cases.json"):
        self.test_cases_path = test_cases_path
    
    def load_test_cases(self) -> List[Dict]:
        """Load test cases from JSON file"""
        try:
            with open(self.test_cases_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("test_cases", [])
        except FileNotFoundError:
            print(f"Test cases file not found: {self.test_cases_path}")
            return []
    
    def run_tests(self, prompt_path: str, sample_size: Optional[int] = None) -> Dict:
        """
        Run golden tests against prompt
        
        In production, this would call Claude API or local LLM.
        For this concept, we simulate the test execution.
        """
        test_cases = self.load_test_cases()
        
        if not test_cases:
            return {"error": "No test cases loaded"}
        
        if sample_size:
            test_cases = self._sample_test_cases(test_cases, sample_size)
        
        results = {
            "total": len(test_cases),
            "passed": 0,
            "failed": 0,
            "details": [],
            "category_breakdown": {}
        }
        
        print(f"Running {len(test_cases)} golden tests...")
        
        for i, test in enumerate(test_cases, 1):
            print(f"   [{i}/{len(test_cases)}] Testing {test['id']}...", end=" ")
            
            # Simulate response generation (replace with actual LLM call in production)
            response = self._generate_response(prompt_path, test["input"])
            
            # Validate against expected elements
            passed = self._validate_response(response, test)
            
            # Track category stats
            category = test["category"]
            if category not in results["category_breakdown"]:
                results["category_breakdown"][category] = {"passed": 0, "total": 0}
            results["category_breakdown"][category]["total"] += 1
            
            if passed:
                results["passed"] += 1
                results["category_breakdown"][category]["passed"] += 1
                print("PASS")
            else:
                results["failed"] += 1
                print("FAIL")
            
            results["details"].append({
                "test_id": test["id"],
                "passed": passed,
                "category": category,
                "input": test["input"][:50]
            })
        
        results["pass_rate"] = results["passed"] / results["total"] if results["total"] > 0 else 0
        return results
    
    def _sample_test_cases(self, test_cases: List[Dict], size: int) -> List[Dict]:
        """Sample test cases ensuring category representation"""
        categories = {}
        for test in test_cases:
            cat = test["category"]
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(test)
        
        sampled = []
        per_category = max(2, size // len(categories))
        for cat, tests in categories.items():
            sampled.extend(tests[:per_category])
        
        return sampled[:size]
    
    def _generate_response(self, prompt_path: str, user_input: str) -> str:
        """
        Generate response using LLM
        
        In production: Call Anthropic API with system prompt
        For concept: Return placeholder
        """
        # TODO: Integrate with Anthropic API
        # message = client.messages.create(
        #     model="claude-sonnet-4-20250514",
        #     max_tokens=500,
        #     system=load_prompt(prompt_path),
        #     messages=[{"role": "user", "content": user_input}]
        # )
        # return message.content[0].text
        
        return "[SIMULATED RESPONSE]"
    
    def _validate_response(self, response: str, test: Dict) -> bool:
        """Validate response against expected elements"""
        # Check expected elements
        passed = all(
            elem.lower() in response.lower() 
            for elem in test["expected_elements"]
        )
        
        # Special validation for escalation tests
        if test["category"] == "escalation_triggers":
            passed = passed and ("ticket" in response.lower() or "escalat" in response.lower())
        
        # Academic integrity tests require policy mention
        if "academic" in test["input"].lower() or "lecture notes" in test["input"].lower():
            passed = passed and "policy" in response.lower()
        
        return passed
    
    def validate_pass_rates(self, results: Dict) -> Tuple[bool, List[str]]:
        """Check if results meet deployment thresholds"""
        failures = []
        
        # Overall pass rate
        if results.get("pass_rate", 0) < PASS_RATE_THRESHOLDS["overall"]:
            failures.append(
                f"Overall pass rate {results.get('pass_rate', 0):.1%} < {PASS_RATE_THRESHOLDS['overall']:.0%}"
            )
        
        # Safety category must be 100%
        if "safety_guidelines" in results.get("category_breakdown", {}):
            safety = results["category_breakdown"]["safety_guidelines"]
            safety_rate = safety["passed"] / safety["total"] if safety["total"] > 0 else 0
            if safety_rate < PASS_RATE_THRESHOLDS["safety"]:
                failures.append(f"Safety category {safety_rate:.1%} < 100%")
        
        # Escalation category must be 100%
        if "escalation_triggers" in results.get("category_breakdown", {}):
            esc = results["category_breakdown"]["escalation_triggers"]
            esc_rate = esc["passed"] / esc["total"] if esc["total"] > 0 else 0
            if esc_rate < PASS_RATE_THRESHOLDS["escalation"]:
                failures.append(f"Escalation category {esc_rate:.1%} < 100%")
        
        return len(failures) == 0, failures
    
    def save_results(self, results: Dict, output_path: str = "test-results.json") -> None:
        """Save test results to JSON file"""
        results["timestamp"] = datetime.now().isoformat()
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)
        print(f"Results saved to {output_path}")


# =============================================================================
# Deployment Workflow
# =============================================================================

class DeploymentManager:
    """Handles deployment with rollback capabilities"""
    
    def __init__(self, environment: Environment = Environment.STAGING):
        self.environment = environment
        self.version_registry = "version_registry.json"
        self.vc = VersionControl()
        self.test_runner = TestRunner()
    
    def deploy_to_staging(self, version: str) -> bool:
        """Deploy to staging environment"""
        print(f"\n Deploying v{version} to STAGING...")
        
        # Run smoke tests (5 critical cases)
        results = self.test_runner.run_tests("prompt.md", sample_size=5)
        
        if results.get("pass_rate", 0) < 1.0:
            print(f"Staging smoke tests failed: {results.get('pass_rate', 0):.1%}")
            return False
        
        print(f"Staging deployment successful")
        self._update_version_registry(version, "staging")
        return True
    
    def deploy_to_production(self, version: str, requires_policy_approval: bool) -> bool:
        """Deploy to production with approval check"""
        if requires_policy_approval:
            if not self._check_policy_approval(version):
                print("Policy approval not obtained")
                return False
        
        print(f"\n Deploying v{version} to PRODUCTION...")
        
        # Deploy with feature flag (10% rollout initially)
        self._enable_feature_flag(version, rollout_percentage=10)
        
        # Monitor first 100 queries (simulated)
        monitoring_ok = self._monitor_deployment(duration_minutes=30)
        
        if not monitoring_ok:
            print("Production monitoring detected issues - initiating rollback")
            self.rollback(version)
            return False
        
        # Full rollout
        self._enable_feature_flag(version, rollout_percentage=100)
        self._update_version_registry(version, "production")
        self.vc.tag_version(version)
        
        print(f"Production deployment complete: v{version}")
        return True
    
    def rollback(self, current_version: str, reason: str = "Unspecified") -> bool:
        """Rollback to previous stable version"""
        previous_version = self.vc.get_previous_version(current_version)
        
        if not previous_version:
            print("No previous version found for rollback")
            return False
        
        print(f"\n  Rolling back from v{current_version} to v{previous_version}...")
        print(f" Reason: {reason}")
        
        # Git rollback
        if not self.vc.rollback_to_version(previous_version):
            return False
        
        # Redeploy previous version
        self._enable_feature_flag(previous_version, rollout_percentage=100)
        self._update_version_registry(previous_version, "production")
        
        # Log incident
        self._log_incident(current_version, previous_version, reason)
        
        return True
    
    def _check_policy_approval(self, version: str) -> bool:
        """Check if policy approval is recorded"""
        approval_file = f"approvals/v{version}_policy_approved.txt"
        try:
            with open(approval_file, "r", encoding="utf-8") as f:
                return True
        except FileNotFoundError:
            return False
    
    def _enable_feature_flag(self, version: str, rollout_percentage: int) -> None:
        """Enable feature flag with rollout percentage"""
        print(f"Feature flag v{version}: {rollout_percentage}% rollout")
        # In production: Call feature flag service (LaunchDarkly, etc.)
    
    def _monitor_deployment(self, duration_minutes: int) -> bool:
        """Monitor deployment for errors"""
        print(f" Monitoring deployment for {duration_minutes} minutes...")
        # In production: Check error rates, user feedback, escalation spikes
        # For concept: Always pass
        return True
    
    def _update_version_registry(self, version: str, environment: str) -> None:
        """Update version registry file"""
        registry = self._load_registry()
        registry["current"][environment] = version
        registry["history"].append({
            "version": version,
            "environment": environment,
            "deployed_at": datetime.now().isoformat()
        })
        
        os.makedirs("versions", exist_ok=True)
        with open(self.version_registry, "w", encoding="utf-8") as f:
            json.dump(registry, f, indent=2)
    
    def _load_registry(self) -> Dict:
        """Load version registry"""
        try:
            with open(self.version_registry, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return {"current": {"staging": "", "production": ""}, "history": []}
    
    def _log_incident(self, from_version: str, to_version: str, reason: str) -> None:
        """Log rollback incident"""
        incident = {
            "type": "rollback",
            "from_version": from_version,
            "to_version": to_version,
            "reason": reason,
            "timestamp": datetime.now().isoformat(),
            "status": "completed"
        }
        
        with open("incidents.json", "a", encoding="utf-8") as f:
            f.write(json.dumps(incident) + "\n")
        print(f"Incident logged: {from_version} → {to_version}")


# =============================================================================
# Change Approval Process
# =============================================================================

class ApprovalManager:
    """Manages change approval workflow"""
    
    def __init__(self):
        self.approvals_file = "approvals/pending_approvals.json"
        os.makedirs("approvals", exist_ok=True)
    
    def request_approval(self, version: str, change_type: ChangeType, 
                         description: str, requester: str) -> str:
        """Submit approval request"""
        required_approvers = APPROVAL_MATRIX.get(change_type, ["engineering"])
        risk_level = RISK_LEVELS.get(change_type, RiskLevel.MEDIUM).value
        
        request = {
            "request_id": hashlib.md5(f"{version}{datetime.now()}".encode()).hexdigest()[:8],
            "version": version,
            "change_type": change_type.value,
            "risk_level": risk_level,
            "description": description,
            "requester": requester,
            "required_approvers": required_approvers,
            "obtained_approvers": [],
            "status": "pending",
            "created_at": datetime.now().isoformat()
        }
        
        self._save_request(request)
        self._notify_approvers(request, required_approvers)
        
        return request["request_id"]
    
    def submit_approval(self, request_id: str, approver: str, role: str) -> bool:
        """Submit approval from stakeholder"""
        requests = self._load_requests()
        
        for request in requests:
            if request["request_id"] == request_id:
                if role in request["required_approvers"]:
                    if approver not in request["obtained_approvers"]:
                        request["obtained_approvers"].append(f"{approver} ({role})")
                        
                        # Check if all approvals obtained
                        if len(request["obtained_approvers"]) >= len(request["required_approvers"]):
                            request["status"] = "approved"
                            self._create_approval_file(request["version"])
                        
                        self._save_requests(requests)
                        return True
        
        return False
    
    def get_approval_status(self, version: str) -> str:
        """Get approval status for a version"""
        requests = self._load_requests()
        for request in requests:
            if request["version"] == version:
                return request["status"]
        return "not_required"
    
    def _notify_approvers(self, request: Dict, approvers: List[str]) -> None:
        """Notify required approvers (email/slack integration)"""
        print(f"Approval request {request['request_id']} sent to: {approvers}")
        # In production: Send email/Slack notification
    
    def _save_request(self, request: Dict) -> None:
        """Save approval request"""
        requests = self._load_requests()
        requests.append(request)
        self._save_requests(requests)
    
    def _load_requests(self) -> List[Dict]:
        """Load pending approval requests"""
        try:
            with open(self.approvals_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return []
    
    def _save_requests(self, requests: List[Dict]) -> None:
        """Save approval requests"""
        with open(self.approvals_file, "w", encoding="utf-8") as f:
            json.dump(requests, f, indent=2)
    
    def _create_approval_file(self, version: str) -> None:
        """Create approval file for deployment check"""
        with open(f"approvals/v{version}_policy_approved.txt", "w", encoding="utf-8") as f:
            f.write(f"Approved at {datetime.now().isoformat()}")
        print(f"Approval file created for v{version}")


# =============================================================================
# Main Workflow
# =============================================================================

def run_update_workflow(change_type: str, version: str, description: str, requester: str) -> None:
    """Main update workflow - orchestrates the full process"""
    
    # Initialize components
    vc = VersionControl()
    test_runner = TestRunner()
    deployer = DeploymentManager()
    approval_mgr = ApprovalManager()
    
    change_type_enum = ChangeType(change_type)
    requires_policy = change_type_enum in [ChangeType.POLICY, ChangeType.SAFETY, ChangeType.ESCALATION]
    
    print("=" * 60)
    print("UniMarketplace Prompt Update Automation")
    print("=" * 60)
    print(f"Change Type: {change_type}")
    print(f"Version: {version}")
    print(f"Description: {description}")
    print(f"Policy Approval Required: {requires_policy}")
    print("=" * 60)
    
    # Step 1: Create branch
    branch = vc.create_branch(f"update-{version}", change_type_enum)
    print(f"Created branch: {branch}")
    
    # Step 2: Run tests on updated prompt
    print("\n Running golden tests...")
    results = test_runner.run_tests("prompt.md", sample_size=12)
    print(f"   Pass Rate: {results.get('pass_rate', 0):.1%}")
    
    passes, failures = test_runner.validate_pass_rates(results)
    if not passes:
        print(" Tests failed:")
        for failure in failures:
            print(f"   - {failure}")
        sys.exit(1)
    
    print(" Tests passed")
    test_runner.save_results(results)
    
    # Step 3: Request approvals if needed
    if requires_policy:
        print("\n Requesting approvals...")
        request_id = approval_mgr.request_approval(
            version, change_type_enum, description, requester
        )
        print(f"   Approval Request ID: {request_id}")
        print(f"   Required: {APPROVAL_MATRIX[change_type_enum]}")
        print("    Waiting for approvals... (manual step in concept)")
    else:
        print("\n No policy approval required for this change type")
    
    # Step 4: Deploy to staging
    print("\n Deploying to staging...")
    if not deployer.deploy_to_staging(version):
        print(" Staging deployment failed")
        sys.exit(1)
    
    # Step 5: Deploy to production (if approved)
    print("\n Deploying to production...")
    if deployer.deploy_to_production(version, requires_policy):
        vc.tag_version(version)
        print(f"\n Deployment complete: v{version}")
    else:
        print("\n Production deployment failed or awaiting approval")


def run_deployment(version: str, environment: str) -> None:
    """Deploy a specific version to an environment"""
    deployer = DeploymentManager()
    env = Environment(environment)
    
    print(f" Deploying v{version} to {environment.upper()}...")
    
    if env == Environment.STAGING:
        success = deployer.deploy_to_staging(version)
    elif env == Environment.PRODUCTION:
        approval_mgr = ApprovalManager()
        requires_approval = approval_mgr.get_approval_status(version) == "pending"
        success = deployer.deploy_to_production(version, requires_approval)
    
    if success:
        print(" Deployment successful")
    else:
        print(" Deployment failed")
        sys.exit(1)


def run_rollback(target: str, reason: str) -> None:
    """Rollback to a specific version"""
    deployer = DeploymentManager()
    success = deployer.rollback(target, reason)
    
    if success:
        print(" Rollback successful")
    else:
        print(" Rollback failed")
        sys.exit(1)


def main():
    """Main entry point with argument parsing"""
    parser = argparse.ArgumentParser(
        description="UniMarketplace Prompt Update Automation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run full update workflow
  python automation-concept.py --change-type safety --version 1.1.1 --description "Fix escalation"
  
  # Deploy to specific environment
  python automation-concept.py --deploy --version 1.1.0 --environment staging
  
  # Rollback to previous version
  python automation-concept.py --rollback --target v1.0.9 --reason "Test failure"
        """
    )
    
    # Workflow mode
    parser.add_argument("--change-type", type=str, 
                        choices=[ct.value for ct in ChangeType],
                        help="Type of change (typo, navigation, transaction, safety, policy, escalation)")
    parser.add_argument("--version", type=str, help="Version number (e.g., 1.1.0)")
    parser.add_argument("--description", type=str, help="Change description")
    parser.add_argument("--requester", type=str, default="developer", help="Requester name/email")
    
    # Deployment mode
    parser.add_argument("--deploy", action="store_true", help="Deploy mode")
    parser.add_argument("--environment", type=str, 
                        choices=["development", "staging", "production"],
                        default="staging", help="Target environment")
    
    # Rollback mode
    parser.add_argument("--rollback", action="store_true", help="Rollback mode")
    parser.add_argument("--target", type=str, help="Target version for rollback")
    parser.add_argument("--reason", type=str, default="Unspecified", help="Rollback reason")
    
    # Test mode
    parser.add_argument("--test", action="store_true", help="Run tests only")
    parser.add_argument("--sample-size", type=int, default=12, help="Number of tests to run")
    
    args = parser.parse_args()
    
    # Determine mode and execute
    if args.rollback and args.target:
        run_rollback(args.target, args.reason)
    elif args.deploy and args.version:
        run_deployment(args.version, args.environment)
    elif args.test:
        test_runner = TestRunner()
        results = test_runner.run_tests("prompt.md", sample_size=args.sample_size)
        test_runner.save_results(results)
        print(f"\nPass Rate: {results.get('pass_rate', 0):.1%}")
    elif args.change_type and args.version:
        run_update_workflow(args.change_type, args.version, args.description or "", args.requester)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()