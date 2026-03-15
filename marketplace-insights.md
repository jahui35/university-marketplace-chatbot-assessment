# Marketplace Domain Knowledge Analysis
## UniMarketplace Chatbot Requirements

---

## Overview

This document demonstrates understanding of the unique challenges, user needs, and operational considerations for a university marketplace platform. Insights are based on NTU Marketplace telegram group's patterns and Singapore university campus contexts.

---

## Common User Pain Points in Student Marketplaces

### 1. Discovery and Search Friction

| Pain Point | Impact | Chatbot Solution |
|------------|--------|------------------|
| Items buried in unstructured feeds | Wasted time scrolling, missed opportunities | Guided search with filters (category, price, location) |
| Unclear item conditions | Mismatched expectations after getting item, disputes | Prompt for condition rating + photo requirements |
| No price guidance | Typical overpricing or underpricing | Suggest fair market range based on similar listings |

### 2. Transaction Coordination Issues

| Pain Point | Impact | Chatbot Solution |
|------------|--------|------------------|
| Scheduling meetup conflicts | Delayed transactions, ghosting | Suggest common free periods, campus safe zones |
| Unclear payment expectations | Awkward negotiations, scams | Standardize payment method guidance (PayNow, Cash on delivery) |
| No-show buyers/sellers | Wasted time and trips, frustration | Reminder notifications, ghosting policy education |

### 3. Listing Creation Barriers

| Pain Point | Impact | Chatbot Solution |
|------------|--------|------------------|
| Don't know what info to include | Incomplete listings, low response | Step-by-step posting wizard with required fields |
| Poor photo quality | Low engagement | Photo tips + minimum requirement enforcement |
| Unclear category selection | Misclassified items | Smart category suggestions based on description |
| Fear of scams when posting | Hesitation to buy | Safety tips embedded in posting flow |

### 4. First-Time User Confusion

| Pain Point | Impact | Chatbot Solution |
|------------|--------|------------------|
| Don't understand verification | Can't post, frustration | Clear .edu.sg requirement explanation |
| Unfamiliar with marketplace norms | Accidental policy violations | Onboarding checklist + guideline summaries |
| Don't know where to start | Abandonment | Menu-driven guidance for common tasks |

---

## Safety and Trust Challenges Specific to Campus Communities

### 1. Identity Verification

| Challenge | Risk | Mitigation |
|-----------|------|------------|
| Fake accounts pretending to be students | Scams from outside campus | Mandatory .edu.sg email verification against university database |
| Shared/borrowed accounts | Untraceable bad actors | One account per student ID, login anomaly detection |

### 2. Physical Safety Concerns

| Challenge | Risk | Mitigation |
|-----------|------|------------|
| Meetup at private residences | Personal safety risk | Block private address sharing, suggest public zones |
| Late-night transactions | Vulnerability to crime | Enforce daylight hours (9am-8pm), flag unusual timing requests |
| Meeting off-campus | No university jurisdiction | Discourage off-campus, provide campus safe zone list |
| Sharing personal contact info | Harassment, doxxing | Keep communication in-app, block phone/WhatsApp sharing |

### 3. Financial Safety

| Challenge | Risk | Mitigation |
|-----------|------|------------|
| Advance payment requests | Payment without delivery | Warn against PayNow before meetup, escrow recommendation |
| Counterfeit goods | Financial loss, legal issues | Block counterfeit keywords, user reporting mechanism |
| Price gouging during peak periods | Exploitation of desperate buyers | Fair pricing guidelines, report inflated prices |
| Trade value disputes | Unfair exchanges | Value assessment guidance, cash top-up option |

### 4. Academic Integrity Risks

| Challenge | Risk | Mitigation |
|-----------|------|------------|
| Selling lecture notes/slides | Copyright violation, policy breach | Block academic material keywords, educate on policy |
| Trading assignment solutions | Undermines learning, cheating | Prohibit academic services, report to academic office |
| Tutoring for payment | Gray area, potential exploitation | Clarify policy, suggest official tutoring channels |
| Selling exam papers | Academic misconduct | Immediate escalation to academic integrity office |

### 5. Community Trust Building

| Challenge | Risk | Mitigation |
|-----------|------|------------|
| Anonymous transactions | Low accountability | Display verified student status, transaction history |
| No reputation system | Can't assess seller reliability | Implement rating/review system, badge for verified users |
| Silent exits after issues | Unresolved disputes | Escalation pathway, moderator intervention |
| Lack of policy awareness | Unintentional violations | In-context policy reminders, searchable guidelines |

---

## Seasonal Patterns and Demand Cycles

### Academic Calendar Impact

| Period | Activity Level | Popular Items | Chatbot Adaptation |
|--------|---------------|---------------|-------------------|
| **Week 1-2 (Add/Drop)** | Peak | Textbooks, calculators, course materials, Hall materials | Prioritize textbook search, quick-posting flow |
| **Week 3-12 (Regular)** | Moderate | Electronics, furniture, hobby items, handmade goods | Standard operations, promote trade features |
| **Week 13-14 (Reading)** | Low | Study materials, last-minute needs | Exam week messaging, reduced notification frequency |
| **Exam Week** | Minimal | Emergency items only | Quiet mode, essential queries only |
| **End of Semester (Hall Clearance)** | Low | Furniture, appliances, dorm items | Bulk listing tools, free pickup coordination |
| **Summer/Winter Break** | Low | High-value items, electronics | Off-campus shipping options, extended meetup windows |
| **Orientation (New Students)** | Peak | Essentials, bundles, starter kits | New student onboarding, bundle deals promotion |
| **Graduation (May/June)** | Peak | Furniture, appliances, course materials, handmade gifts, graduation bouquets | Graduation sale tags, bulk disposal coordination |

### Hall Clearance Period (Critical)

| Challenge | Solution |
|-----------|----------|
| Students need to dispose of items quickly | "Free pickup" category, bulk listing wizard |
| Oversupply causes price crashes | Fair pricing alerts, donation option suggestions |
| Limited storage until pickup | Coordinate pickup timing, temporary storage info |
| High scam risk during rush | Enhanced verification, priority moderation |

### Textbook Exchange Cycles

| Semester | Action |
|----------|--------|
| Before Semester 1 | Promote textbook buyback from seniors |
| Week 1-2 | Peak textbook sales, module-specific search |
| Mid-Semester | Steady used book market |
| End of Semester | Collect textbooks for next cycle |

---

## Integration Needs with University Systems

### 1. Identity and Authentication

| Integration | Purpose | Implementation |
|-------------|---------|----------------|
| **.edu.sg Email Verification** | Confirm student status | API check against university directory |
| **Student ID Validation** | Prevent duplicate accounts | One account per student Matriculation ID number |
| **Graduation Date Sync** | Account lifecycle management | Auto-expire or convert to alumni tagged account|

### 2. Campus Infrastructure

| Integration | Purpose | Implementation |
|-------------|---------|----------------|
| **Academic Calendar API** | Seasonal chatbot behavior | Adjust prompts based on current week |
| **Campus Map System** | Safe meetup location suggestions | Embed LT1, Koufu, Library coordinates |
| **Hall Management System** | Dorm policy enforcement | Know hall clearance dates, storage rules |
| **Facilities Booking** | Reserve meetup spaces | Optional booking of transaction zones |

### 3. Safety and Support Systems

| Integration | Purpose | Implementation |
|-------------|---------|----------------|
| **University Security** | Emergency escalation | Direct line for serious safety incidents |
| **Academic Integrity Office** | Policy violation reporting | Auto-notify for academic material sales |
| **Student Support Services** | Vulnerable user assistance | Referral for financial hardship cases |
| **IT Help Desk** | Technical issue escalation | Ticket system integration for bugs |

---

## Key Chatbot Requirements Derived from Domain Analysis

### Functional Requirements

| ID | Requirement | Priority | Rationale |
|----|-------------|----------|-----------|
| FR-01 | Guide users through listing creation with required fields | High | Reduces incomplete listings |
| FR-02 | Provide safe meetup location suggestions | High | Physical safety is critical |
| FR-03 | Detect and block prohibited item keywords | High | Legal and policy compliance |
| FR-04 | Escalate safety concerns to human moderators | High | Risk mitigation |
| FR-05 | Support sale, trade, and sale-or-trade listing types | Medium | Flexibility for users |
| FR-06 | Adapt responses based on academic calendar period | Medium | Contextual relevance |
| FR-07 | Verify .edu.sg email before enabling posting | High | Community trust |
| FR-08 | Provide fair value assessment for trades | Medium | Prevent exploitation |

### Non-Functional Requirements

| ID | Requirement | Target | Rationale |
|----|-------------|--------|-----------|
| NFR-01 | Response time | < 2 seconds | User experience |
| NFR-02 | Availability | 99.5% uptime | Critical support channel |
| NFR-03 | Data privacy | No personal info storage | Compliance, trust |
| NFR-04 | Scalability | Handle 10x peak during hall clearance | Seasonal demand |
| NFR-05 | Accessibility | Mobile-first design | Student device usage |
| NFR-06 | Language support | English + Singlish understanding | Local communication norms |

### Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| User issue resolution without escalation | ≥70% | Conversation analytics |
| Safety violation detection rate | 100% | Moderation review |
| User satisfaction score | >0.6 sentiment | Post-chat survey |
| Average conversation length | 3-5 turns | Analytics dashboard |
| Policy education effectiveness | <10% repeat violations | Violation tracking |

---

## Assumptions Made

1. **University Context**: Analysis assumes a Singapore university (e.g., NTU, NUS) with similar campus structures and policies
2. **Student Population**: Primarily undergraduate students living in on-campus halls
3. **Platform Scope**: Peer-to-peer marketplace, not B2C or official university sales
4. **Moderation Capacity**: Human moderators available during business hours with escalation coverage
5. **Technical Integration**: University systems have APIs available for integration (SSO, email verification)
6. **Legal Framework**: Singapore law applies (Trade Marks Act for counterfeits, etc.)
