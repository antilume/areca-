# System 04: Candidate Reactivation System

## 1. Executive Summary
The Candidate Reactivation System (CRS) is designed to maximize the value of the agency's existing internal database (ATS). It uses automated outreach workflows to re-engage past candidates who have become "stale," ensuring that high-value candidates are updated and kept warm for future roles. By using multi-channel communication (Email, SMS, WhatsApp) and AI-driven personalization, the CRS turns a static candidate pool into a dynamic, recurring asset.

## 2. Problem Statement & Business Context
Recruitment agencies often have databases of 100k+ candidates, yet only 5-10% are "fresh" and active. Candidates in the database are "warm leads," but they are often ignored in favor of cold, external sourcing. The CRS solves the "database decay" problem by automating the "keep-in-touch" process, improving candidate experience, and reducing the cost-per-hire by utilizing already-owned data.

## 3. System Architecture Overview
The CRS is a **Stateful Outreach Orchestration Engine**.
- **Staleness Monitor:** A background job (PostgreSQL/Redis) that flags profiles based on a "Staleness Score" (calculated by days-since-last-activity and profile completeness).
- **Outreach Orchestrator:** Powered by **Temporal.io**, this manages multi-day, multi-channel communication sagas, handling retries, wait states, and human-in-the-loop triggers.
- **Engagement Engine:** An LLM service (GPT-4o) that generates personalized messages based on a candidate's past history and potential fit for current roles.

## 4. Scraping Layer (Multi-Board) / Data Acquisition
The CRS "scrapes" internal interaction data:
- **Email History:** Syncing recruiter-candidate threads to detect the last "real" human interaction.
- **ATS Event Logs:** Tracking past interview feedback and application history.
- **LinkedIn Profile Polling:** Periodically checking for job changes on LinkedIn to automatically update the internal "Golden Profile."

## 5. Deduplication & Quality Filter Engine
- **Profile Collision Detection:** When a candidate is reactivated, the system checks for any new duplicate profiles created in the interim from external scrapers (System 02/03).
- **Sentiment Filter:** Uses NLP to analyze past interview notes and emails; candidates with "Strong Reject" or "Negative Cultural Fit" flags are excluded from automated reactivation campaigns.

## 6. Decision-Maker Linking Engine
Reactivated candidates are automatically linked to hiring managers (from System 01) who are currently hiring for roles (from System 02) that match the candidate's *newly updated* skills and preferences.

## 7. Data Models & Schema
- `StalenessFlag`:
    - `candidate_id`: UUID
    - `last_activity_at`: DateTime
    - `staleness_score`: Float (0.0 to 1.0)
    - `primary_outreach_channel`: Enum (EMAIL, SMS, WHATSAPP)
- `OutreachSequence`:
    - `id`: UUID
    - `candidate_id`: UUID
    - `sequence_step`: Integer (e.g., Day 1: Email, Day 4: SMS)
    - `status`: Enum (PENDING, SENT, RESPONDED, OPTED_OUT)
    - `last_response_text`: Text (Normalized via NLP)

## 8. Workflow Diagrams (ASCII)
```text
[ Staleness Monitor (Cron) ]
      |
      v
[ Candidate Segmentation ] ---> [ Excluded (Negative Sentiment) ]
      |
      v
[ Temporal.io Saga ]
      |
      +--- [ Step 1: AI Email Outreach ]
      |            |
      |            v (No Response)
      +--- [ Step 2: AI SMS Follow-up ]
      |            |
      |            v (Candidate Response)
[ NLP Response Handler ] ---> [ Update Profile Store ]
      |
      v
[ Trigger: System 03 Matcher ]
```

## 9. Tech Stack & Tools
- **Orchestration:** Temporal.io (Go/Python SDK).
- **Messaging API:** Twilio (SMS/WhatsApp), SendGrid (Email).
- **NLP:** OpenAI GPT-4o (Personalization and Intent Analysis).
- **Backend:** Python (FastAPI).

## 10. Anti-Bot Evasion Strategy (Evasion & Resilience)
- **Email Deliverability:** Using dedicated IPs, managing SPF/DKIM/DMARC, and implementing "warm-up" sequences to maintain high sender reputation.
- **Frequency Capping:** Ensuring a candidate never receives more than X messages per month across all agency recruiters.
- **Natural Language Jitter:** Generating slightly different versions of the same outreach message to avoid being flagged by carrier-side spam filters.

## 11. Legal & Compliance Considerations
- **GDPR Article 21 (Right to Object):** Providing a clear "One-Click Opt-Out" in every communication.
- **Legitimate Interest:** Ensuring the outreach is relevant to the candidate's career and clearly identifies the agency.
- **TCPA (Telephone Consumer Protection Act):** Obtaining explicit consent for SMS/WhatsApp outreach.

## 12. MVP vs. Production Scope
- **MVP:** Email-only outreach; rule-based personalization; daily batch processing.
- **Production:** Multi-channel (Email/SMS/WhatsApp/LinkedIn InMail); AI-driven hyper-personalization; real-time response handling and profile updating via Temporal.io sagas.

## 13. Error Handling & Resilience
- **Bounce Handling:** Automatically marking a candidate's email as "Inactive" if a hard bounce is detected.
- **Conflict Handling:** Automatically pausing an outreach saga if a recruiter manually emails the candidate during the campaign.

## 14. Performance & Scale Targets
- **Re-Engagement Rate:** > 20% of stale candidates responding with updated info.
- **Outreach Capacity:** Handling 10,000+ concurrent outreach sagas per day.
- **Response Latency:** Processing and updating the profile within 1 minute of receiving a candidate's response.
