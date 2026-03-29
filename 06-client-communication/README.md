# System 06: Automated Client Communication

## 1. Executive Summary
The Automated Client Communication (ACC) system streamlines the interaction between the recruitment agency and hiring managers. It automates the creation of high-impact candidate "One-Pagers," manages the submission workflow, and provides a white-labeled portal for clients to review shortlists and provide real-time feedback. By removing administrative friction from the "Selling" phase, the ACC accelerates the placement cycle and improves the agency's professional image.

## 2. Problem Statement & Business Context
Recruiters currently spend 20-30% of their day on "admin" tasks like reformatting resumes, drafting submission emails, and chasing hiring managers for feedback. These manual tasks delay the interview process and increase the risk of "candidate drop-off." The ACC solves this by using AI to generate punchy summaries and providing a centralized portal that makes "reviewing a candidate" as easy as clicking a button.

## 3. System Architecture Overview
The ACC is a **Submission Lifecycle Management Engine**.
- **One-Pager Generator:** An LLM service that synthesizes the candidate's CV (from System 05) and the recruiter's interview notes into a professional candidate profile.
- **Magic Link Portal:** A secure, web-based dashboard for hiring managers that requires no login (secured via unique, time-limited JWTs).
- **Feedback Loop Engine:** A real-time WebSocket service that notifies the recruiter the moment a client opens a profile or leaves a comment.

## 4. Scraping Layer (Multi-Board) / Data Acquisition
The ACC "scrapes" client engagement data:
- **Portal Telemetry:** Tracking "Time-on-Profile," "Section Clicks," and "Download Events" to gauge hiring manager interest.
- **Client ATS Feedback:** If the client has an integrated ATS (e.g., Greenhouse, Lever), the ACC pushes candidate data and pulls back status changes and interview scores.

## 5. Deduplication & Quality Filter Engine
- **Profile Sanitization:** Automatically removes all candidate contact details (Email, Phone, LinkedIn) to ensure compliance with the agency's fee-protection policy.
- **Feedback Sentiment Analysis:** An LLM that categorizes client comments (e.g., "The candidate is too junior," "Let's interview them") into structured data for System 08 analytics.

## 6. Decision-Maker Linking Engine
The ACC facilitates the final link between the candidate and the hiring manager decision-maker (from System 01). It ensures that the submission is delivered to the *correct* manager via their preferred channel (Email, Slack, or MS Teams).

## 7. Data Models & Schema
- `CandidateOnePager`:
    - `id`: UUID
    - `candidate_id`: UUID
    - `recruiter_summary`: Text (AI-generated)
    - `skill_highlights`: JSONB
    - `is_anonymized`: Boolean
- `ClientSubmission`:
    - `id`: UUID
    - `job_id`: UUID
    - `manager_id`: UUID
    - `portal_token`: String (Magic Link JWT)
    - `status`: Enum (SENT, OPENED, REVIEWED, FEEDBACK_RECEIVED)
    - `client_notes`: Text

## 8. Workflow Diagrams (ASCII)
```text
[ Shortlisted Candidate ] --- (LLM) ---> [ One-Pager Generator ]
                                                |
                                          v Sanitizer v
                                                |
[ CRM Submission ] --- (JWT Gen) ---> [ Magic Link Email ]
                                                |
[ Client Dashboard ] <--- (WebSocket) --- [ Hiring Manager Interaction ]
      |
      v
[ Feedback Event ] ---> [ System 07 Scheduler ]
      |
      v
[ Dashboard / System 08 ]
```

## 9. Tech Stack & Tools
- **Frontend:** Next.js / Tailwind CSS (White-labeled portal).
- **Backend:** Node.js (FastAPI) or Go.
- **Magic Links:** JSON Web Tokens (JWT) with short TTL (72h).
- **Notifications:** SendGrid / Postmark / Slack Webhooks.

## 10. Anti-Bot Evasion Strategy (Evasion & Resilience)
- **Link Security:** Magic links are single-device bound and include IP-address whitelisting options for sensitive clients.
- **Email Reputation:** Ensuring submission emails don't hit the hiring manager's spam filter by using dedicated sub-domains and strict DMARC/BIMI enforcement.
- **Rate-Limiting Notifications:** Digesting multiple candidate submissions into a single daily alert to prevent "inbox fatigue."

## 11. Legal & Compliance Considerations
- **PII Redaction:** Strict enforcement of contact-info redaction for non-exclusive candidates.
- **Data Retention:** Automatically expiring portal links and anonymizing candidate data after a placement is made or the job is closed.
- **Audit Logging:** Every view and feedback event is logged with a timestamp for potential fee disputes.

## 12. MVP vs. Production Scope
- **MVP:** Automated One-Pager generation; email-based feedback; basic JWT-secured portal.
- **Production:** Full white-labeling (client branding); real-time WebSocket notifications; automated Slack/Teams integrations; two-way ATS sync with the client's internal system.

## 13. Error Handling & Resilience
- **Link Recall:** Ability for the recruiter to "kill" a magic link if a submission was made in error.
- **Feedback Fallback:** If the client replies to the email rather than using the portal, an LLM-based "Email-to-Feedback" parser updates the system status.

## 14. Performance & Scale Targets
- **Submission Latency:** < 5 minutes from "Shortlist Approval" to "Client Inbox."
- **Portal Performance:** < 300ms page-load time for global hiring managers.
- **Feedback Loop:** Sub-second sync between client action and recruiter dashboard notification.
