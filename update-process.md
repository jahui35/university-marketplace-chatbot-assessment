# Prompt Update Process - UniMarketplace Assistant

## Overview

This document defines the standard operating procedure for updating the UniMarketplace chatbot prompt as marketplace features evolve, policies change, or improvements are identified through testing and user feedback.

---

## Guiding Principles

1. **Safety First** — Any change affecting safety guardrails requires human approval
2. **Test Before Deploy** — All updates must pass the golden test suite (≥95% pass rate)

---

## Version Control Integration

### Branching Strategy

| Branch | Purpose | Protection |
|--------|---------|------------|
| `main` | Production-ready prompt | Protected, requires PR + approval |
| `staging` | Pre-deployment testing | Protected, auto-deploy from PR merge |
| `feature/*` | Individual changes | Developer-owned, deleted after merge |
| `hotfix/*` | Urgent safety/policy fixes | Expedited review path |

### Commit Convention

```
[TYPE][CATEGORY] Brief description

TYPE: feat | fix | docs | policy | safety
CATEGORY: nav | trans | safety | esc | edge
```

**Examples:**
```
[safety][esc] Add academic office notification for integrity violations
[fix][nav] Correct mark-as-sold workflow steps
```

### Version Tagging

```
v{MAJOR}.{MINOR}.{PATCH}

MAJOR: Breaking changes to prompt structure
MINOR: New features or capabilities
PATCH: Bug fixes or minor improvements
```

**Example:** `v1.1.0 → v1.1.1` (patch fix for escalation wording)


## Automated Testing Pipeline

### Test Execution Triggers

| Trigger | Test Scope | Required Pass Rate |
|---------|-----------|-------------------|
| Pull Request | 12-case sample | 95% |
| Pre-Deployment | Full 44-case suite | 95% |
| Post-Deployment | 5 critical smoke tests | 100% |
| Monthly Regression | Full suite + new cases | 95% |

### Test Categories Validated

| Category | Tests | Critical Elements |
|----------|-------|------------------|
| Basic Navigation | 8 | Posting, searching, account management |
| Transaction Support | 8 | Payment safety, trade coordination |
| Safety & Guidelines | 10 | Prohibited items, academic integrity |
| Escalation Triggers | 8 | Ticket ID generation, moderator handoff |
| Edge Cases | 10 | Ambiguous input, Singlish, XSS handling |

---

## Deployment Workflow

### Stages

| Stage | Environment | Approval | Rollback Window |
|-------|-------------|----------|-----------------|
| 1. Development | Local/Feature Branch | None | N/A |
| 2. Staging | Test Environment | Engineering Lead | Immediate |
| 3. Production | Live Chatbot | Policy Lead (if policy change) | 5 minutes |

### Deployment Checklist

- [ ] Golden tests pass (≥95% overall)
- [ ] Safety category: 100% pass
- [ ] Escalation category: 100% pass
- [ ] Policy approval obtained (if applicable)
- [ ] Rollback plan documented
- [ ] Stakeholders notified (for policy changes)
- [ ] Version tag created
- [ ] `CHANGELOG.md` updated

### Feature Flag Strategy

For high-risk changes, use gradual rollout:

```yaml
feature_flags:
  new_escalation_flow:
    enabled: true
    rollout_percentage: 10   # Start at 10%
    increment: 10            # Increase by 10% per hour
    max: 100
```

---

## Rollback Capabilities

### Automatic Rollback Triggers

| Condition | Action | Notification |
|-----------|--------|-------------|
| Golden test pass rate < 95% | Block deployment | Engineering team |
| Safety category < 100% | Block deployment | Engineering + Policy |
| Staging smoke test failure | Auto-rollback | On-call engineer |
| Production error rate > 5% | Auto-rollback | Engineering + Policy |
| User complaint spike | Manual review → Rollback | Support team |
| Escalation rate spike > 20% | Manual review → Rollback | Product team |

### Rollback Procedure

```bash
# Immediate rollback to previous version
./scripts/rollback.sh --version v1.0.9

# Verify rollback
./scripts/smoke-test.sh --env production
```

### Version Registry

| Version | Deployed Date | Status | Rollback Target |
|---------|--------------|--------|----------------|
| v1.1.0 | 2026-03-15 | Production | v1.0.9 |
| v1.0.9 | 2026-03-01 | Archived | v1.0.8 |
| v1.0.8 | 2026-02-15 | Archived | v1.0.7 |

---

## Change Approval Process

### Approval Matrix

| Change Type | Engineering | Policy | Security | Academic Office | Timeline |
|-------------|:-----------:|:------:|:--------:|:---------------:|----------|
| Typo/Grammar | ✅ | ❌ | ❌ | ❌ | Same day |
| Navigation Flow | ✅ | ❌ | ❌ | ❌ | 1–2 days |
| Transaction Logic | ✅ | ✅ | ❌ | ❌ | 2–3 days |
| Safety Guardrails | ✅ | ✅ | ✅ | ❌ | 3–5 days |
| Academic Policy | ✅ | ✅ | ✅ | ✅ | 5–7 days |
| Escalation Triggers | ✅ | ✅ | ✅ | ❌ | 3–5 days |

### Policy Change Workflow

1. Open PR with change description and rationale
2. Assign approvers per the matrix above
3. Await all required approvals
4. Merge to `staging` and run full test suite
5. Schedule production deployment with stakeholder notification

### Documentation Requirements

Every PR must include:

- Change description and rationale
- Affected test cases (updated or added)
- Risk assessment (low / medium / high)
- Rollback plan if issues occur
- Stakeholders notified (for policy changes)
- Version bump (MAJOR / MINOR / PATCH)

### Approval Tracking

```json
{
  "pr_number": 42,
  "change_type": "safety_guardrails",
  "approvals": {
    "engineering": { "approved_by": "eng-lead", "date": "2026-03-14" },
    "policy": { "approved_by": "policy-lead", "date": "2026-03-14" },
    "security": { "approved_by": "sec-lead", "date": "2026-03-15" }
  }
}
```

---

## Monitoring & Observability

### Post-Deployment Metrics

| Metric | Threshold | Alert Recipient |
|--------|-----------|----------------|
| Error Rate | < 2% | Engineering |
| Escalation Rate | < 15% | Support Team |
| User Satisfaction | > 0.6 sentiment | Product Team |
| Response Time | < 2 seconds | Engineering |
| Safety Violation Miss | 0 | Security + Policy |
| Academic Policy Violation | 0 | Academic Office |

### Alerting Channels

| Severity | Channel | Response Time |
|----------|---------|--------------|
| Critical (Safety/Escalation failures) | Slack `#chatbot-alerts` + PagerDuty | 15 minutes |
| Warning (Performance degradation) | Slack `#chatbot-monitoring` | 1 hour |
| Info (Deployment complete) | Slack `#chatbot-deployments` | N/A |

### Monitoring Dashboard

Key metrics to track in real-time:

- Requests per minute
- Error rate by category
- Escalation ticket volume
- Average response time
- User satisfaction score
- Top user queries

---

## Continuous Improvement

### Monthly Review Cadence

| Week | Activity | Output |
|------|----------|--------|
| 1 | Analyze production query logs for gaps | Gap analysis report |
| 2 | Add 5–10 new golden tests from real queries | Updated `test-cases.json` |
| 3 | Identify prompt optimization opportunities | Optimization backlog |
| 4 | Plan next sprint's improvements | Sprint plan |

### Metrics to Track

| Metric | Baseline | Target | Frequency |
|--------|----------|--------|-----------|
| Golden Test Pass Rate | 95% | 98% | Per deployment |
| Coverage (intents) | 90% | 95% | Monthly |
| Time to Rollback | 5 min | 2 min | Per incident |
| Policy Update Lead Time | 5 days | 3 days | Quarterly |
| User Satisfaction | 0.7 | 0.8 | Weekly |

### Feedback Loops

- **User Feedback** — In-chat satisfaction survey after resolved conversations
- **Moderator Feedback** — Weekly review of escalated cases for prompt gaps
- **Support Team Feedback** — Top 10 user complaints reviewed monthly
- **Engineering Feedback** — Test failure patterns analyzed per sprint

---

## Appendix: File Locations

| File | Purpose | Location |
|------|---------|----------|
| `prompt.xml` | Current production prompt | Repository root |
| `test-cases.json` | Golden test definitions | Repository root |
| `automation-concept.py` | Test runner and deployment script | Repository root |
| `CHANGELOG.md` | Version history | Repository root |
| `version_registry.json` | Current and previous versions | Repository root |
| `approvals/` | Approval request records | Subdirectory |
| `incidents.json` | Rollback and incident log | Repository root |

