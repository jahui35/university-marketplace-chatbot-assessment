# Testing Framework for UniMarketplace Assistant

## Overview

This testing framework validates the UniMarketplace chatbot prompt performance using golden tests—predefined test cases with expected outputs that ensure consistent, reliable chatbot behavior across updates. The framework covers buying, selling, trading, and university context-specific enforcements.

## Testing Approach

### Philosophy

I employed a safety-first, regression-prevention testing strategy. Every prompt update must pass all existing golden tests before deployment, ensuring that new features or policy changes do not break existing functionality or compromise safety guardrails.

### Test Case Structure

Each test case includes:
- id: Unique identifier with category prefix (nav_, trans_, safety_, esc_, edge_)
- category: One of five test categories
- input: User query or scenario
- expected_elements: Array of required response components
- success_criteria: Human-readable success definition
- edge_case: Boolean flag for unusual scenarios

### Test Categories

#### 1. Basic Navigation (8 tests)

Validates core platform functionality:
- Posting listings (sale, trade, or both)
- Searching and filtering by transaction type
- Account management and verification
- Listing CRUD operations
- Contact mechanisms

Coverage: Ensures users can complete fundamental marketplace tasks

#### 2. Transaction Support (8 tests)

Tests transaction-related guidance:
- Payment methods and safety
- Trade proposal processes
- Pickup coordination at campus safe zones
- Value disparity handling
- Dispute resolution

Coverage: Validates safe transaction facilitation for both sales and trades

#### 3. Safety & Guidelines (10 tests)

Verifies policy enforcement:
- Prohibited items (vapes, alcohol, prescription meds, counterfeit)
- Academic integrity violations (lecture notes, exam papers, tutoring services)
- Personal information protection
- Meetup safety
- Reporting mechanisms

Coverage: Critical for community safety, legal compliance, and academic integrity

#### 4. Escalation Triggers (8 tests)

Confirms proper handoff to human moderators:
- Harassment detection
- Fraud recognition
- Trade disputes
- Academic integrity violations
- Threats and illegal activity
- Repeat violations

Coverage: Ensures high-risk situations receive human oversight

#### 5. Edge Cases (10 tests)

Tests robustness against unusual inputs:
- Ambiguous queries
- Gibberish or nonsensical input
- Singlish or slang inputs
- Multi-intent messages
- Security probing (XSS attempts)
- Impossible constraint sets
- Meta-questions about bot behavior

Coverage: Validates graceful handling of unexpected scenarios

## Execution Methodology

### Automated Testing Pipeline

### Conceptual Automation Design (Pseudo-Code)

The following pseudo-code illustrates how this testing framework could be automated in production. For this assessment, tests were executed manually via Claude's web interface due to time & money constraints, but the validation logic remains identical.

```python
def run_golden_tests(prompt_version):
    results = {
        "total": len(test_cases),
        "passed": 0,
        "failed": 0,
        "details": []
    }
    
    for test in test_cases:
        response = chatbot.generate_response(
            prompt=prompt_version,
            user_input=test["input"]
        )
        
        #Checks for expected elements
        passed = all(
            element in response for element in test["expected_elements"]
        )
        
        #Validation for escalation tests
        if test["category"] == "escalation_triggers":
            passed = passed and "ticket_id" in response
        
        #Academic integrity tests require policy education
        if "academic" in test["input"].lower() or "lecture notes" in test["input"].lower():
            passed = passed and "policy" in response.lower()
        
        #Edge case handling validation
        if test["edge_case"]:
            passed = passed and validate_graceful_handling(response)
        
        results["details"].append({
            "test_id": test["id"],
            "passed": passed,
            "response_sample": response[:200]
        })
        
        if passed:
            results["passed"] += 1
        else:
            results["failed"] += 1
    
    return results