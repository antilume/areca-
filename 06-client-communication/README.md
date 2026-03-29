# System 06: Automated Client Communication

## 1. Executive Summary
The Automated Client Communication (ACC) system streamlines the interaction between the recruitment agency and their hiring manager clients. It automates the generation of candidate "One-Pagers," manages feedback loops for shortlists, and provides a white-labeled portal for clients to review and approve candidates.

## 2. Problem Statement & Business Context
Recruiters spend too much time formatting resumes, writing "sales" summaries, and chasing hiring managers for feedback. ACC reduces this friction, speeding up the "time-to-interview" and improving the professional image of the agency.

## 3. System Architecture Overview
ACC is a **Template-Driven Communication Engine**.
- **Content Generator:** Uses an LLM to summarize resumes (from System 05) into a punchy "Recruiter Note."
- **Client Portal:** A secure, web-based dashboard where hiring managers view shortlists.
- **Notification Bus:** Manages email/Slack alerts to clients when new candidates are ready.

## 4. Scraping Layer (Multi-Board) / Data Acquisition
ACC "scrapes" client-side data:
- **Client ATS:** Syncing feedback from the client's internal systems (e.g., Lever, Workday).
- **Communication Threads:** Ingesting feedback from email replies (via IMAP/GMAIL API).

## 5. Deduplication & Quality Filter Engine
- **Profile Sanitization:** Automatically removes candidate contact info (Email/Phone) before sharing with clients (preventing "backdoor" hiring).
- **Feedback Normalizer:** Converts "I like him" or "No" into structured ratings (1-5 stars) using an LLM classifier.

## 6. Decision-Maker Linking Engine
ACC maps candidates (from System 05) to the specific hiring manager (from System 01) through a "Submission Workflow." It ensures the *right* manager gets the *right* candidate at the *right* time.

## 7. Data Models & Schema
- `ClientSubmission`: (id, job_id, candidate_id, manager_id, status, client_feedback_text, recruiter_note)
- `ClientPortalConfig`: (company_id, logo_url, custom_domain, notification_preferences)
- `SubmissionEvent`: (submission_id, action, timestamp, actor_id)

## 8. Workflow Diagrams (ASCII)
```text
[ Top Candidates ] -> [ AI Summary Gen ] -> [ Submission Email ]
                                                    |
                                            (Click to Portal)
                                                    |
                                            v Client Review v
                                                    |
                                            [ Feedback Loop ] -> [ System 07 ]
```

## 9. Tech Stack & Tools
- **Portal:** React / Tailwind CSS.
- **Backend:** Node.js (Express) or Python (Django).
- **Messaging:** SendGrid (Email), Slack Webhooks.
- **Summarization:** OpenAI GPT-4o (for high-quality professional writing).

## 10. Anti-Bot Evasion Strategy (Evasion & Resilience)
- **Link Security:** Unique, time-limited, and trackable "Magic Links" for client access.
- **Email Deliverability:** Monitoring sender reputation to ensure client submissions don't end up in spam.
- **Rate-Limited Notifications:** Grouping multiple candidate submissions into a single daily digest to avoid "inbox fatigue."

## 11. Legal & Compliance Considerations
- **Data Privacy:** Ensuring candidates' PII is only shared with authorized clients.
- **Audit Trail:** Maintaining a record of who viewed which candidate and when (crucial for fee disputes).
- **Terms of Service:** Clearly stating the agency's ownership of the candidate lead during the submission phase.

## 12. MVP vs. Production Scope
- **MVP:** Automated "Recruiter Note" generation and manual email submissions.
- **Production:** Full white-labeled client portal with interactive feedback and integrated scheduling.

## 13. Error Handling & Resilience
- **Recall Capability:** Allowing recruiters to "Un-submit" a candidate if an error is found.
- **Notification Retries:** If a client's mail server bounces, notifying the recruiter via an internal alert.

## 14. Performance & Scale Targets
- **Submission Speed:** < 5 minutes from candidate shortlist to client submission.
- **Feedback Latency:** Real-time sync between the client portal and the agency's internal dashboard.
- **User Satisfaction:** > 4.5/5 client rating for the submission experience.
