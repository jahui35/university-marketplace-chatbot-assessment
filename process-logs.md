# PROCESS_LOG.md
## Thinking Process Documentation - UniMarketplace Chatbot Assessment

**Candidate:** Tan Jia Hui 
**Assessment Start:** 2026-03-13 09:00 SGT  
**Assessment End:** 2026-03-15 15:30 SGT  
**Total Time:** ~5-6 hours (Done slowly over the course of 2 days)

---

## Initial Approach 

### First Impressions
- Read the full PDF requirements carefully
- Noted the 2.5-3 hour target but planned for slight overrun given iteration needs
- Identified the 5 core components and prioritized by weight: Prompt Design (45 min) and Golden Tests (60 min) got first focus

### Repository Setup
- Created folder structure immediately to avoid last-minute organization stress
- Decided to work top-down: prompt → tests → automation → domain → prototype → docs
- Chose to use XML for prompt structure after weighing vs. markdown (XML better for hierarchical logic)

### Key Early Decisions
1. **Safety-first philosophy**: Escalation triggers and academic integrity enforcement would be non-negotiable in all components
2. **NTU-specific context**: Would embed campus details (LT1, Koufu, .edu.sg) throughout, not just in one section
3. **Trading support**: Added early after re-reading requirements—buy/sell/trade all needed coverage

---

## Prompt Design Phase

### Iteration 1: Basic Structure 
- Drafted role definition, core capabilities, user scenarios
- Used XML tags for clear section separation
- Included initial safety guardrails (prohibited items, escalation keywords)

### Iteration 2: Adding Trading Logic 
- Realized initial prompt only covered buy/sell
- Added `<trading_capabilities>` section with trade modes (sale_only, trade_only, sale_or_trade)
- Created conditional rules for trade value disparity and ghosting prevention

### Iteration 3: Academic Integrity Enforcement
- Added `<academic_integrity_enforcement>` after considering university context
- Listed prohibited academic items (lecture notes, exam papers, solutions)
- Created detection keywords and escalation pathway to academic office

### Challenges Faced
- Balancing prompt verbosity vs. token efficiency: XML is clear but adds tokens
- Deciding how much detail to put in prompt vs. external documentation
- Ensuring conditional logic was specific enough to trigger correctly but flexible enough for varied phrasing

### Resolution
- Kept XML structure for maintainability; noted token optimization as future improvement
- Used `<note>` tags for explanatory context that doesn't affect model behavior
- Tested conditional logic mentally against sample queries before moving on

---

## Golden Test Design Phase 

### Test Case Strategy 
- Decided on 44 total cases: 8-12 per category to exceed minimum (5) while staying under max (50)
- Prioritized safety-critical tests first (academic integrity, scam detection)
- Created ID convention: `{category}_{number}` for easy sorting and reference

### Writing Test Cases 
- Started with Basic Navigation: posting, searching, account creation
- Added Transaction Support: payment safety, trade proposals, value disparity
- Safety & Guidelines: prohibited items, academic materials, reporting
- Escalation Triggers: fraud, threats, academic violations
- Edge Cases: gibberish, Singlish, XSS attempts, multi-intent queries

### Validation Logic Design
- Defined `expected_elements` as keyword lists for semantic matching
- Added category-specific rules: escalation tests require ticket ID, academic tests require "policy" mention
- Decided on pass thresholds: 100% for safety/escalation, 95% overall

### Challenges Faced
- Defining "expected elements" granularity: too strict causes false failures, too loose misses violations
- Ensuring edge cases were truly unusual, not just normal flows with different wording
- Balancing test coverage with time constraint

### Resolution
- Used keyword-based semantic checks with category-specific overrides
- Reviewed edge cases against definition: "unusual requests, multiple topics, unclear intent"
- Accepted that 44 cases was sufficient coverage; noted expansion as future work

---

## Automation & Update Process Phase 

### Workflow Design 
- Created mermaid diagram first to visualize the full flow
- Defined branching strategy: main/staging/feature/hotfix
- Established commit convention and version tagging scheme

### Approval Matrix 
- Mapped change types to required approvers (engineering, policy, security, academic office)
- Added timeline estimates for each change type
- Created documentation requirements for PRs

### Rollback Strategy
- Defined automatic rollback triggers (test failures, error spikes)
- Created simple rollback script concept
- Added version registry for tracking deployments

### Challenges Faced
- Making the workflow realistic but not over-engineered for an intern assessment
- Balancing automation detail with pseudo-code acceptability
- Ensuring approval process was thorough but not bureaucratic

### Resolution
- Focused on core requirements: version control, testing, deployment, rollback, approval
- Used Python classes to demonstrate structure without full implementation
- Noted that production would add more monitoring and alerting detail

---

## Marketplace Domain Knowledge Phase 

### Pain Point Analysis
- Listed common student marketplace frustrations: discovery friction, transaction coordination, listing barriers
- Mapped each pain point to chatbot solution in table format for clarity

### Safety & Trust Challenges
- Identified campus-specific risks: fake accounts, unsafe meetups, academic integrity violations
- Proposed mitigations aligned with prompt design (verification, safe zones, policy education)

### Seasonal Patterns & Integrations 
- Mapped academic calendar to demand cycles (add/drop peak, hall clearance, exam quiet)
- Listed university system integrations: SSO, email verification, campus map, academic calendar API

### Challenges Faced
- Avoiding generic marketplace advice; ensuring campus-specific relevance
- Balancing breadth (covering all topics) with depth (actionable insights)

### Resolution
- Used NTU examples throughout (LT1, Koufu, .edu.sg) to ground analysis
- Structured content in tables for scannability; added recommendations section for synthesis

---

## Prototype Phase 

### Platform Selection 
- Evaluated options: Hugging Face Spaces, Botpress, Claude web interface, custom Flask
- Chose Hugging Face + Gradio for fastest public URL + code transparency

### Implementation 
- Created Gradio ChatInterface with example prompts
- Implemented rule-based intent matching for 5 core flows (sell, buy, trade, safety, help)
- Embedded NTU-specific responses (safe zones, academic policy)

### Testing & Screenshots 
- Tested 5 representative cases from test-cases.json
- Captured screenshots of key responses
- Saved to `resources/` folder with descriptive filenames

### Challenges Faced
- Time pressure: 30 minutes is tight for deployment + testing
- Balancing prototype simplicity with demonstrating key logic
- Ensuring responses matched expected elements from test cases

### Resolution
- Used rule-based matching to guarantee response consistency within time constraint
- Documented clearly that production would use LLM API; prototype validates logic flow
- Focused testing on safety-critical flows to demonstrate understanding

---

## Documentation Phase 

### Sample-Chatbot-info.md 
- Documented platform rationale, testing results, assumptions, limitations
- Added production roadmap to show forward thinking
- Included reflection on prototype trade-offs

### README.md + PROCESS_LOG.md 
- Wrote README with overview, structure, assumptions, time breakdown, reflection
- Created PROCESS_LOG (this file) to capture thinking process as required
- Final repository structure check and commit

### Final Review
- Verified all required files present
- Checked that `PROCESS_LOG.md` was marked mandatory in submission
- Confirmed prototype URL was accessible and shared correctly

---

## Key Learnings

1. **Prompt Engineering is Iterative**: My first prompt draft was functional but missing trading logic and academic integrity. Iteration based on requirement re-reading significantly improved coverage.

2. **Testing GenAI Requires New Thinking**: Traditional exact-match testing doesn't work well for LLM outputs. Semantic keyword checking with category-specific rules was more effective.

3. **Documentation is Part of the Product**: Clear `PROCESS_LOG.md` and `README.md` aren't just administrative—they demonstrate communication skills and systematic thinking that matter for engineering roles.

4. **Constraints Drive Creativity**: The 30-minute prototype limit forced me to prioritize core logic over polish, which actually resulted in a clearer demonstration of understanding.

5. **Safety Cannot Be an Afterthought**: Embedding safety guardrails and escalation pathways from the start (not as a final step) ensured they were consistent across all components.

---

## What I Would Do Differently With More Time

1. **Automate Test Execution**: Instead of manual testing via Claude web interface, integrate Claude API in `automation-concept.py` for reproducible, scalable validation.

2. **Add Multi-Turn Tests**: Current tests are single-turn; real conversations need context tracking. Would add conversation flow test cases.

3. **Expand Edge Case Coverage**: Add more multilingual tests (Mandarin, Malay) and cultural nuance scenarios for Singapore context.

4. **Implement Real Deployment Pipeline**: Instead of conceptual GitHub Actions YAML, set up actual CI/CD with test gating.

5. **User Testing**: Recruit 2-3 student peers to test the prototype and provide feedback on usability and clarity.

---

## Final Self-Assessment

| Component | Confidence | Reason |
|-----------|------------|--------|
| Prompt Design | High | Clear XML structure, comprehensive coverage, safety-first logic |
| Golden Tests | High | 44 cases, thoughtful validation logic, realistic pass thresholds |
| Automation Design | Medium-High | Conceptual but complete workflow; would benefit from real API integration |
| Domain Knowledge | High | Campus-specific insights, actionable recommendations, integration awareness |
| Prototype | Medium | Demonstrates logic flow; rule-based vs. LLM is documented limitation |
| Documentation | High | Clear, structured, transparent about assumptions and limitations |

**Overall Confidence**: High—I believe this submission demonstrates strong prompt engineering, testing methodology, automation thinking, and domain understanding aligned with the assessment goals.

