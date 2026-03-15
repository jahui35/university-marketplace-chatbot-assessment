# Chatbot Prototype Documentation
## UniMarketplace Assistant

---

## Prototype URL

**Platform:** Hugging Face Spaces (Gradio)  
**URL:** https://huggingface.co/spaces/jahui35/unimarketplace-chatbot  
**Status:** Public Demo - Build successful 2026-03-15  
**Access:** No login required; open to all users for testing

---

## Platform Selection Rationale

### Why Hugging Face Spaces + Gradio?

| Criteria | Hugging Face Spaces | Alternatives Considered |
|----------|---------------------|------------------------|
| **Cost** | Free tier sufficient for prototype | Botpress (conversation limits), Streamlit (similar) |
| **Deployment Speed** | ~5 minutes from code to public URL | Custom hosting (hours of setup) |
| **Public Accessibility** | Automatic HTTPS URL, no auth required | Localhost (not shareable), requires tunneling |
| **Code Transparency** | Full `app.py` visible in Files tab | No-code builders (opaque logic) |
| **Scalability** | Handles moderate traffic with auto-scaling | Local testing only |
| **Integration** | Python-native, easy Gradio + API wiring | JavaScript frameworks require more setup |

### Why Not Other Platforms?

| Platform | Reason Rejected |
|----------|-----------------|
| **Botpress** | Free tier limited to 1,000 conversations/month; requires account setup and visual flow design time |
| **Dialogflow CX** | Steeper learning curve; better suited for enterprise voice bots |
| **Custom Flask/FastAPI + React** | Requires hosting infrastructure, CORS setup, and frontend/backend separation—beyond 30-minute scope |
| **Telegram/Discord Bot** | Requires platform-specific API setup, phone/server verification, and users must join external apps |
| **Vercel + Next.js** | More complex deployment pipeline; Gradio provides chat UI out-of-the-box |

### Key Decision Factors

1. **Assessment Constraints**: 30-minute time limit required the fastest path from code to public URL
2. **Assessor Accessibility**: Public URL with no login ensures assessors can test immediately
3. **Demonstration of Implementation**: Writing `app.py` shows understanding of routing logic, not just configuration
4. **Cost Efficiency**: Free tier sufficient for prototype; no credit card required
5. **Extensibility**: Gradio app can be replaced with API call to Claude without changing deployment workflow

---

## Assumptions

### Technical Assumptions

1. **LLM Integration**: The prototype uses rule-based intent matching for demonstration. In production, `chatbot_response()` would call the Claude API with the full system prompt from `prompt.md` to generate dynamic, context-aware responses.

2. **Stateless Conversations**: Each user message is processed independently. The prototype does not maintain conversation history. Production would require session management (e.g., Redis) for multi-turn dialogues.

3. **No Authentication**: User identity is not verified. Production would integrate with NTU SSO and enforce `.edu.sg` email verification before enabling posting.

4. **No Persistent Storage**: The prototype does not connect to a database. Listing data and user profiles are not stored. Production would require PostgreSQL/MongoDB for data persistence.

5. **Static Safe Zones**: Safe meetup locations are hardcoded. Production would fetch these from a campus map API for dynamic updates.

6. **Demo Ticket IDs**: Escalation responses generate placeholder IDs. Production would integrate with a real ticketing system (Jira, Zendesk) for trackable cases.

7. **Rate Limiting**: The prototype has no abuse prevention. Production would implement rate limiting to prevent spam.

8. **Image Handling**: The prototype does not support image upload. Production would integrate cloud storage + vision API for photo moderation.

### User Experience Assumptions

9. **English-First**: Responses are in English only. Production would benefit from Singlish/NLU support for local communication norms.

10. **Mobile-First Design**: Gradio is responsive but not fully optimized for all mobile screens. Production would use a custom mobile frontend.

11. **User Technical Literacy**: Users are assumed to understand basic chatbot interactions. Production would include onboarding tooltips.

12. **Moderator Availability**: Escalation implies immediate human review. Production would implement queue management and fallback resources.

### Policy and Compliance Assumptions

13. **Policy Stability**: University policies are assumed static. Production would require a policy management system for non-technical updates.

14. **Legal Jurisdiction**: Singapore law applies (e.g., Trade Marks Act). Production would need legal review for cross-border transactions.

15. **Data Privacy**: The prototype does not log conversations. Production would implement PDPA-compliant logging and anonymization.
