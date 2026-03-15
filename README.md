# Govtech-SystemEng-TanJiaHui

# UniMarketplace Chatbot Assessment Submission
## Systems Engineer: EPS GenAI Chatbot Intern Take-Home Assessment

**Candidate:** Tan Jia Hui 
**Submission Date:** 2026-03-15  
**Repository:** https://github.com/jahui35/university-marketplace-chatbot-assessment  
**Prototype Demo:** https://huggingface.co/spaces/jahui35/unimarketplace-chatbot (If the chatbot is down, please do contact me, the website may be reloading)

---

## Overview

This repository contains my submission for the Systems Engineer: EPS GenAI Chatbot intern assessment. The task was to design a chatbot for a university marketplace platform where students can buy, sell, and trade items within their campus community.

### Approach Summary

I took a **structured, safety-first approach** to this assessment:

1. **Prompt Design**: Used XML-based hierarchical formatting to create a maintainable, testable system prompt with clear separation of concerns (role, capabilities, safety, escalation).

2. **Testing Strategy**: Developed 44 golden test cases across 5 categories, with a framework that prioritizes safety-critical validation (100% pass required for safety/escalation categories).

3. **Automation Design**: Created a conceptual update workflow with version control, automated testing, deployment gates, and rollback capabilities—designed for real-world maintainability.

4. **Domain Understanding**: Analyzed campus-specific challenges (academic integrity, seasonal demand, physical safety) to ensure the chatbot aligns with university community needs.

5. **Prototype**: Built a functional demo using Hugging Face Spaces + Gradio to demonstrate implementation understanding within the 30-minute constraint.

---

## Instructions for Reviewing Each Component

### 1. Prompt Design (`prompt.xml`, `prompt-analysis.md`)
- Open `prompt.xml` to see the full XML-structured system prompt
- Key sections: `<role_definition>`, `<task_specifications>`, `<safety_guardrails>`, `<escalation_protocol>`
- Read `prompt-analysis.md` for rationale behind XML formatting, safety-first logic, and NTU context integration

### 2. Golden Test Design (`test-cases.json`, `testing-framework.md`, `testing-result.md`)
- `test-cases.json`: 44 test cases across 5 categories (8-12 per category)
- `testing-framework.md`: Methodology, validation logic, CI/CD integration concept
- `testing-result.md`: Results from 12 representative manual tests via Claude web interface (95.5% pass rate)

### 3. Automation & Update Process (`update-process.md`, `automation-concept.py`)
- `update-process.md`: Workflow diagram (mermaid), branching strategy, approval matrix
- `automation-concept.py`: Python script with VersionControl, TestRunner, DeploymentManager, ApprovalManager classes

### 4. Marketplace Domain Knowledge (`marketplace-insights.md`)
- Analysis of pain points, safety challenges, seasonal patterns, and university system integrations
- Includes functional/non-functional requirements and success metrics

### 5. Prototype (`Sample-Chatbot-info.md`, `resources/`)
- Live demo: https://huggingface.co/spaces/jahui35/unimarketplace-chatbot
- `Sample-Chatbot-info.md`: Platform rationale, testing results, assumptions, limitations
- `resources/`: Screenshots of key conversation flows

### 6. Thinking Process (`PROCESS_LOG.md`)
- Mandatory documentation of decision-making throughout the assessment
- Includes time tracking, challenges, and iterative refinements

---

## Assumptions Made About the University Marketplace

1. **Institution**: Analysis assumes a Singapore university (e.g., NTU or NUS) with on-campus halls, `.edu.sg` email verification, and academic integrity policies.

2. **User Base**: Primarily undergraduate students; transactions are peer-to-peer.

3. **Legal Framework**: Singapore law applies (e.g., Trade Marks Act for counterfeits, PDPA for data privacy).

4. **Moderation Capacity**: Human moderators available during business hours with escalation coverage for urgent issues.

5. **Technical Integration**: University systems (SSO, email verification, academic calendar) have APIs and databases available for integration.

6. **Platform Scope**: Focus on physical item exchange; digital goods (except permitted textbooks) and academic services are prohibited.

---

## Time Breakdown of Effort Allocation

| Component | Allocated Time | Actual Time | Notes |
|-----------|---------------|-------------|-------|
| Prompt Design & Engineering | 45 min | around 1 hour 30 min | Iterated on XML structure and trading logic, tested with Claude online application to check for additional features needed |
| Golden Test Design | 60 min | around 1 Hour 15 min | Added academic integrity test cases |
| Automation & Update Process | 20 min | around 1 hour | Expanded approval matrix and rollback details |
| Marketplace Domain Knowledge | 15 min | 20 min | Added seasonal patterns and integration table |
| Prototype Development | 30 min | around 1 hour | Hugging Face deployment + screenshot capture, used my existing OpenAI credits for AI API component |
| README + PROCESS_LOG | ~15 min | 20 min | Final documentation and reflection |

---

## Next Steps If This Were a Real Project

### Phase 1: Core Integration (2-3 weeks)
- [ ] Integrate Claude API for full LLM response generation
- [ ] Add conversation memory with Redis session storage
- [ ] Implement `.edu.sg` email verification via university API
- [ ] Connect to PostgreSQL database for listing persistence

### Phase 2: Safety & Compliance (1-2 weeks)
- [ ] Integrate with university ticketing system for real escalation
- [ ] Add academic integrity office webhook notifications
- [ ] Implement rate limiting and abuse detection
- [ ] Add PDPA-compliant conversation logging

### Phase 3: Enhancement (2-3 weeks)
- [ ] Multilingual support (Singlish, Mandarin) via translation API
- [ ] Image upload + vision API moderation for listing photos
- [ ] Analytics dashboard (Grafana) for usage patterns
- [ ] Mobile-optimized React frontend replacement for Gradio

### Phase 4: Scale & Monitor (Ongoing)
- [ ] Load testing for hall clearance peak periods
- [ ] A/B testing framework for prompt optimization
- [ ] User feedback loop integration
- [ ] Quarterly policy review and prompt updates

---

## Personal Reflection: Most Challenging Component

**Golden Test Design** was the most challenging component, and here's why:

1. **Balancing Coverage vs. Time**: Creating 44 meaningful test cases across 5 categories in 60 minutes required rapid prioritization. I focused on safety-critical scenarios first (academic integrity, scam detection) before expanding to edge cases.

2. **Defining "Expected Elements"**: Determining the right granularity for validation was tricky. Too specific (exact wording) would fail on semantically correct responses; too vague would miss policy violations. I settled on keyword-based semantic checks with category-specific rules.

3. **Academic Integrity Nuance**: Distinguishing between allowed items (personal textbooks) and prohibited materials (lecture notes, exam papers) required careful test case wording to avoid false positives while enforcing policy.

**What I Learned**: Testing GenAI prompts is fundamentally different from traditional software testing. Success requires thinking in terms of semantic intent, policy boundaries, and graceful degradation, instead of just exact output matching. This shifted my mindset from "does it work?" to "does it work safely and helpfully?"

---

## Three Alternative Approaches Considered and Rejected

### 1. Markdown-Only Prompt Structure
**Considered**: Using plain markdown with headers and bullet points instead of XML tags.  
**Rejected Because**: XML provides clearer hierarchical nesting for conditional logic and makes it easier to parse sections programmatically (e.g., extracting `<safety_guardrails>` for automated policy checks). Markdown is more human-readable but less machine-structured.

### 2. Full LLM API Integration in Prototype
**Considered**: Calling Claude API directly in the Gradio app for dynamic responses.  
**Rejected Because**: The timeand money prototype constraint, instead i used my existing OpenAI API key that i had previously to use for this project

### 3. Botpress or Dialogflow for Chatbot Platform
**Considered**: Using a dedicated chatbot builder with visual flow design.  
**Rejected Because**: These platforms add setup time (account creation, visual flow design) and abstract away the code-level understanding the assessment seeks to evaluate. Gradio + Python demonstrates direct implementation skill while still achieving a public, shareable URL.

---

## My Experience with University Marketplaces

### As a Buyer
- **Safety Awareness**: I've declined meetup requests for private hall rooms and preferred public zones like library foyers—validating the need for enforced safe location guidance.
- **Ghosting of Sellers**: Many sellers that i've arranged a meetup with in school failed to show up to the meetup and failed to reply on the day of the meetup itself and afterward. This wasted my time and proved to be a frustrating experience
- **Price Sensitivity**: I've seen many students mark up their prices for unopened goods and though that it was not very fair. As a student budget, I've compared prices across platforms and hence i put a value on chatbot guidance on fair market ranges. 

### As a Seller
- **Listing Friction**: I've abandoned listings when unsure what details to include. A guided posting flow (like the one in `prompt.md`) would have reduced this friction.
- **Ghosting of Buyers**: On top of sellers, i've experienced no-show buyers, highlighting the need for reminder notifications and clear platform policies.
- **Hall Clearance Rush**: During end-of-semester clearance, I needed to list multiple items quickly. Bulk listing tools and "free pickup" coordination (mentioned in `marketplace-insights.md`) would have been valuable.

### Key Insight
I personally think that University marketplaces aren't just transactional, they're community-building tools. The chatbot must balance efficiency with trust-building, policy enforcement with education, and automation with human oversight. My design prioritizes safety and clarity because a single negative experience can erode campus-wide trust in the platform.

---

## Getting in Touch

If you have questions about this submission or would like to discuss my approach, please reach out via the submission portal or email. I welcome the opportunity to walk through any component in more detail.

**Thank you for considering my application.** 
